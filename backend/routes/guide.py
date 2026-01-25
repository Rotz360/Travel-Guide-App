"""
API routes for travel guide generation
"""
from fastapi import APIRouter, HTTPException
from models.schemas import GuideRequest, TravelGuide, LocationDetail, DayItinerary, DayActivity, ImageInfo
from services.ai_service import (
    generate_location_details,
    generate_itinerary as ai_generate_itinerary
)
from services.image_service import get_location_images
from services.itinerary_service import (
    optimize_route,
    calculate_route_info,
    calculate_days_per_destination,
    get_coordinates
)
from services.recommendations_service import generate_all_recommendations

router = APIRouter()


@router.post("/api/generate-guide", response_model=TravelGuide)
async def generate_travel_guide(request: GuideRequest):
    """
    Generate a complete travel guide with itinerary, images, and recommendations
    
    Args:
        request: GuideRequest with destinations, days, and preferences
        
    Returns:
        Complete TravelGuide object
    """
    try:
        destinations = request.destinations
        total_days = request.days or (len(destinations) * 3)  # Default 3 days per destination
        preferences = request.preferences or ""
        
        # Step 1: Optimize route if multiple destinations
        if len(destinations) > 1:
            destinations = await optimize_route(destinations)
        
        # Step 2: Generate location details for each destination
        location_details = []
        for dest in destinations:
            # Get AI-generated details
            details = await generate_location_details(dest)
            
            # Get images
            images = await get_location_images(dest, count=4)
            main_image = None
            additional_images = []
            
            if images:
                main_image_data = images[0]
                main_image = ImageInfo(
                    url=main_image_data["url"],
                    alt_text=main_image_data["alt_text"],
                    photographer=main_image_data.get("photographer")
                )
                
                # Additional images
                for img_data in images[1:]:
                    additional_images.append(ImageInfo(
                        url=img_data["url"],
                        alt_text=img_data["alt_text"],
                        photographer=img_data.get("photographer")
                    ))
            
            # Get coordinates
            coords = await get_coordinates(dest)
            
            location = LocationDetail(
                name=details.get("name", dest),
                description=details.get("description", ""),
                highlights=details.get("highlights", []),
                main_image=main_image,
                additional_images=additional_images,
                coordinates=coords
            )
            location_details.append(location)
        
        # Step 3: Generate itinerary
        itinerary_data = await ai_generate_itinerary(destinations, total_days, preferences)
        
        # Convert to DayItinerary objects
        itinerary = []
        for day_data in itinerary_data:
            activities = [
                DayActivity(
                    time=act.get("time", ""),
                    activity=act.get("activity", ""),
                    description=act.get("description", ""),
                    location=act.get("location", day_data.get("location", "")),
                    duration=act.get("duration")
                )
                for act in day_data.get("activities", [])
            ]
            
            day = DayItinerary(
                day_number=day_data.get("day_number", 1),
                date=day_data.get("date"),
                title=day_data.get("title", ""),
                activities=activities,
                location=day_data.get("location", "")
            )
            itinerary.append(day)
        
        # Step 4: Generate recommendations
        recommendations = await generate_all_recommendations(destinations)
        
        # Step 5: Calculate route information
        route_info = await calculate_route_info(destinations)
        
        # Create the complete guide
        guide = TravelGuide(
            destinations=location_details,
            itinerary=itinerary,
            recommendations=recommendations,
            route_info=route_info,
            total_days=total_days
        )
        
        return guide
        
    except Exception as e:
        print(f"Error generating travel guide: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate travel guide: {str(e)}"
        )


@router.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "travel-guide-api"}
