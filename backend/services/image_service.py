"""
Image service using Unsplash API for location images
"""
import os
import httpx
from typing import Optional, List, Dict
from dotenv import load_dotenv

load_dotenv()

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
UNSPLASH_API_URL = "https://api.unsplash.com"


async def get_location_images(
    location: str, 
    count: int = 3
) -> List[Dict[str, str]]:
    """
    Fetch images for a location from Unsplash
    
    Args:
        location: Location name to search for
        count: Number of images to fetch (max 10)
        
    Returns:
        List of image dicts with url, alt_text, and photographer
    """
    if not UNSPLASH_ACCESS_KEY:
        # Return placeholder if no API key
        return [{
            "url": f"https://source.unsplash.com/800x600/?{location.replace(' ', ',')}",
            "alt_text": f"Image of {location}",
            "photographer": None
        }]
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{UNSPLASH_API_URL}/search/photos",
                params={
                    "query": location,
                    "per_page": min(count, 10),
                    "orientation": "landscape"
                },
                headers={
                    "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
                },
                timeout=10.0
            )
            
            if response.status_code == 200:
                data = response.json()
                images = []
                
                for photo in data.get("results", []):
                    images.append({
                        "url": photo["urls"]["regular"],
                        "alt_text": photo.get("alt_description") or f"Image of {location}",
                        "photographer": photo["user"]["name"]
                    })
                
                return images if images else _get_fallback_images(location, count)
            else:
                return _get_fallback_images(location, count)
                
    except Exception as e:
        print(f"Error fetching images: {e}")
        return _get_fallback_images(location, count)


def _get_fallback_images(location: str, count: int) -> List[Dict[str, str]]:
    """Generate fallback placeholder images"""
    search_term = location.replace(" ", ",")
    return [{
        "url": f"https://source.unsplash.com/800x600/?{search_term},{i}",
        "alt_text": f"Image of {location}",
        "photographer": None
    } for i in range(count)]


async def get_recommendation_image(place_name: str, category: str) -> Optional[Dict[str, str]]:
    """
    Fetch a single image for a recommendation
    
    Args:
        place_name: Name of the place
        category: Category (sleep, eat, curiosity)
        
    Returns:
        Image dict or None
    """
    # Create a more specific search query
    category_keywords = {
        "sleep": "hotel accommodation",
        "eat": "restaurant food",
        "curiosity": "attraction landmark"
    }
    
    search_query = f"{place_name} {category_keywords.get(category, '')}"
    images = await get_location_images(search_query, count=1)
    
    return images[0] if images else None
