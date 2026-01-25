"""
Pydantic models for request/response validation
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class Destination(BaseModel):
    """Single destination input"""
    name: str = Field(..., description="Destination name (e.g., 'Rome, Italy')")


class GuideRequest(BaseModel):
    """Request model for generating a travel guide"""
    destinations: List[str] = Field(..., min_items=1, description="List of destination names")
    days: Optional[int] = Field(None, ge=1, le=30, description="Number of days for the trip")
    preferences: Optional[str] = Field(None, description="User preferences (e.g., 'budget travel', 'luxury', 'adventure')")


class ImageInfo(BaseModel):
    """Image information"""
    url: str
    alt_text: str
    photographer: Optional[str] = None


class Recommendation(BaseModel):
    """A single recommendation (hotel, restaurant, or attraction)"""
    name: str
    description: str
    category: str  # 'sleep', 'eat', 'curiosity'
    price_level: Optional[str] = None  # '$', '$$', '$$$'
    why_recommended: str
    image: Optional[ImageInfo] = None


class LocationDetail(BaseModel):
    """Detailed information about a location"""
    name: str
    description: str
    highlights: List[str]
    main_image: Optional[ImageInfo] = None
    additional_images: List[ImageInfo] = []
    coordinates: Optional[dict] = None  # {"lat": float, "lng": float}


class DayActivity(BaseModel):
    """Activity for a specific day"""
    time: str  # e.g., "Morning", "Afternoon", "Evening"
    activity: str
    description: str
    location: str
    duration: Optional[str] = None


class DayItinerary(BaseModel):
    """Itinerary for a single day"""
    day_number: int
    date: Optional[str] = None
    title: str
    activities: List[DayActivity]
    location: str  # Main location for the day


class TravelGuide(BaseModel):
    """Complete travel guide response"""
    destinations: List[LocationDetail]
    itinerary: List[DayItinerary]
    recommendations: dict = Field(
        ..., 
        description="Recommendations organized by category"
    )  # {"sleep": [...], "eat": [...], "curiosities": [...]}
    route_info: Optional[dict] = None  # Distance, travel times between locations
    total_days: int
