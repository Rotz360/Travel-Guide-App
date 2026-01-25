"""
Recommendations service - orchestrates Apify (real data) and AI services
"""
from typing import List, Dict
from services.apify_service import (
    get_attractions,
    get_restaurants,
    get_accommodations,
    APIFY_ENABLED
)
from services.ai_service import generate_recommendations as ai_generate_recommendations
from services.image_service import get_recommendation_image
from models.schemas import Recommendation, ImageInfo


async def generate_all_recommendations(
    destinations: List[str]
) -> Dict[str, List[Recommendation]]:
    """
    Generate recommendations for all categories across all destinations
    Uses Apify for real Google Maps data when available, falls back to AI
    
    Args:
        destinations: List of destination names
        
    Returns:
        Dict with 'sleep', 'eat', and 'curiosities' keys
    """
    all_recommendations = {
        "sleep": [],
        "eat": [],
        "curiosities": []
    }
    
    # Generate recommendations for each destination
    for destination in destinations:
        if APIFY_ENABLED:
            # Use real Google Maps data via Apify
            print(f"Fetching real data from Google Maps for {destination}")
            
            # Get real accommodations
            sleep_places = await get_accommodations(destination, max_results=3)
            for place in sleep_places:
                image = None
                if place.get("image_url"):
                    image = ImageInfo(
                        url=place["image_url"],
                        alt_text=f"Photo of {place['name']}",
                        photographer=None
                    )
                
                recommendation = Recommendation(
                    name=place["name"],
                    description=place.get("description") or f"Rated {place.get('rating', 'N/A')} stars with {place.get('reviews_count', 0)} reviews",
                    category="sleep",
                    price_level=place.get("price_level"),
                    why_recommended=f"Highly rated on Google Maps ({place.get('rating', 0)}/5 from {place.get('reviews_count', 0)} reviews)",
                    image=image
                )
                all_recommendations["sleep"].append(recommendation)
            
            # Get real restaurants
            eat_places = await get_restaurants(destination, max_results=3)
            for place in eat_places:
                image = None
                if place.get("image_url"):
                    image = ImageInfo(
                        url=place["image_url"],
                        alt_text=f"Photo of {place['name']}",
                        photographer=None
                    )
                
                recommendation = Recommendation(
                    name=place["name"],
                    description=place.get("description") or f"{place.get('cuisine', 'Restaurant')} - Rated {place.get('rating', 'N/A')} stars",
                    category="eat",
                    price_level=place.get("price_level"),
                    why_recommended=f"Top-rated {place.get('cuisine', 'dining')} ({place.get('rating', 0)}/5 from {place.get('reviews_count', 0)} reviews)",
                    image=image
                )
                all_recommendations["eat"].append(recommendation)
            
            # Get real attractions for curiosities
            attraction_places = await get_attractions(destination, max_results=3)
            for place in attraction_places:
                image = None
                if place.get("image_url"):
                    image = ImageInfo(
                        url=place["image_url"],
                        alt_text=f"Photo of {place['name']}",
                        photographer=None
                    )
                
                recommendation = Recommendation(
                    name=place["name"],
                    description=place.get("description") or f"Popular {place.get('category', 'attraction')} in {destination}",
                    category="curiosity",
                    price_level=place.get("price_level"),
                    why_recommended=f"Must-see attraction ({place.get('rating', 0)}/5 from {place.get('reviews_count', 0)} reviews)",
                    image=image
                )
                all_recommendations["curiosities"].append(recommendation)
        else:
            # Fallback to AI-generated recommendations
            print(f"Using AI-generated recommendations for {destination} (Apify not available)")
            
            for category in ["sleep", "eat", "curiosity"]:
                recs = await ai_generate_recommendations(destination, category)
                
                # Convert to Recommendation objects and add images
                for rec_data in recs:
                    # Get image for this recommendation
                    image_data = await get_recommendation_image(
                        rec_data.get("name", destination),
                        category
                    )
                    
                    image = None
                    if image_data:
                        image = ImageInfo(
                            url=image_data["url"],
                            alt_text=image_data["alt_text"],
                            photographer=image_data.get("photographer")
                        )
                    
                    recommendation = Recommendation(
                        name=rec_data.get("name", ""),
                        description=rec_data.get("description", ""),
                        category=category,
                        price_level=rec_data.get("price_level"),
                        why_recommended=rec_data.get("why_recommended", ""),
                        image=image
                    )
                    
                    # Add to appropriate category
                    if category == "curiosity":
                        all_recommendations["curiosities"].append(recommendation)
                    else:
                        all_recommendations[category].append(recommendation)
    
    return all_recommendations
