"""
Apify service for fetching real data from Google Maps
Uses the compass/crawler-google-places scraper
"""
import os
from typing import List, Dict, Optional
from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
APIFY_ENABLED = bool(APIFY_API_TOKEN)

# Initialize Apify client
client = ApifyClient(APIFY_API_TOKEN) if APIFY_ENABLED else None


async def search_google_places(
    query: str,
    max_results: int = 10,
    min_rating: float = 4.0
) -> List[Dict]:
    """
    Search Google Places using Apify scraper
    
    Args:
        query: Search query (e.g., "restaurants in Paris")
        max_results: Maximum number of results to return
        min_rating: Minimum rating filter (0-5)
        
    Returns:
        List of place dictionaries with details
    """
    if not APIFY_ENABLED:
        print("Apify not enabled - token not found")
        return []
    
    try:
        # Prepare the Actor input
        run_input = {
            "searchStringsArray": [query],
            "maxCrawledPlacesPerSearch": max_results,
            "language": "en",
            "skipClosedPlaces": True,
            "allPlacesNoSearchAction": False,
            # Don't scrape reviews to save credits
            "reviews": False,
            # Get images
            "images": True,
            # Skip additional info to save time
            "additionalInfo": False,
        }
        
        # Run the Actor and wait for it to finish
        print(f"Running Apify scraper for: {query}")
        run = client.actor("compass/crawler-google-places").call(run_input=run_input)
        
        # Fetch results from the dataset
        results = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            # Filter by rating
            rating = item.get("totalScore", 0)
            if rating >= min_rating:
                results.append(item)
        
        print(f"Found {len(results)} places with rating >= {min_rating}")
        return results[:max_results]
        
    except Exception as e:
        print(f"Error fetching from Apify: {e}")
        return []


async def get_attractions(destination: str, max_results: int = 5) -> List[Dict]:
    """
    Get top attractions for a destination
    
    Args:
        destination: Destination name
        max_results: Maximum results
        
    Returns:
        List of attraction details
    """
    query = f"tourist attractions in {destination}"
    places = await search_google_places(query, max_results=max_results, min_rating=4.2)
    
    # Transform to our format
    attractions = []
    for place in places:
        attractions.append({
            "name": place.get("title", ""),
            "description": place.get("description", ""),
            "rating": place.get("totalScore", 0),
            "reviews_count": place.get("reviewsCount", 0),
            "address": place.get("address", ""),
            "website": place.get("website"),
            "phone": place.get("phone"),
            "image_url": place.get("imageUrl") or (place.get("images", [{}])[0].get("url") if place.get("images") else None),
            "coordinates": {
                "lat": place.get("location", {}).get("lat"),
                "lng": place.get("location", {}).get("lng")
            } if place.get("location") else None,
            "price_level": place.get("priceLevel"),
            "category": place.get("categoryName", "Attraction")
        })
    
    return attractions


async def get_restaurants(destination: str, max_results: int = 5) -> List[Dict]:
    """
    Get top restaurants for a destination
    
    Args:
        destination: Destination name
        max_results: Maximum results
        
    Returns:
        List of restaurant details
    """
    query = f"best restaurants in {destination}"
    places = await search_google_places(query, max_results=max_results, min_rating=4.0)
    
    # Transform to our format
    restaurants = []
    for place in places:
        # Determine price level
        price_level = "$$$"  # default
        if place.get("priceLevel"):
            price_level = "$" * len(place.get("priceLevel"))
        
        restaurants.append({
            "name": place.get("title", ""),
            "description": place.get("description", ""),
            "rating": place.get("totalScore", 0),
            "reviews_count": place.get("reviewsCount", 0),
            "address": place.get("address", ""),
            "website": place.get("website"),
            "phone": place.get("phone"),
            "image_url": place.get("imageUrl") or (place.get("images", [{}])[0].get("url") if place.get("images") else None),
            "price_level": price_level,
            "cuisine": place.get("categoryName", "Restaurant"),
            "coordinates": {
                "lat": place.get("location", {}).get("lat"),
                "lng": place.get("location", {}).get("lng")
            } if place.get("location") else None,
        })
    
    return restaurants


async def get_accommodations(destination: str, max_results: int = 5) -> List[Dict]:
    """
    Get top accommodations for a destination
    
    Args:
        destination: Destination name
        max_results: Maximum results
        
    Returns:
        List of accommodation details
    """
    query = f"hotels in {destination}"
    places = await search_google_places(query, max_results=max_results, min_rating=4.0)
    
    # Transform to our format
    accommodations = []
    for place in places:
        # Determine price level
        price_level = "$$"  # default
        if place.get("priceLevel"):
            price_level = "$" * len(place.get("priceLevel"))
        
        accommodations.append({
            "name": place.get("title", ""),
            "description": place.get("description", ""),
            "rating": place.get("totalScore", 0),
            "reviews_count": place.get("reviewsCount", 0),
            "address": place.get("address", ""),
            "website": place.get("website"),
            "phone": place.get("phone"),
            "image_url": place.get("imageUrl") or (place.get("images", [{}])[0].get("url") if place.get("images") else None),
            "price_level": price_level,
            "type": place.get("categoryName", "Hotel"),
            "coordinates": {
                "lat": place.get("location", {}).get("lat"),
                "lng": place.get("location", {}).get("lng")
            } if place.get("location") else None,
        })
    
    return accommodations
