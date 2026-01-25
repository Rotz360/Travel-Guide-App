"""
Itinerary service for route optimization and travel calculations
"""
from typing import List, Dict, Optional
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import asyncio


# Initialize geocoder
geolocator = Nominatim(user_agent="travel_guide_app")


async def get_coordinates(location: str) -> Optional[Dict[str, float]]:
    """
    Get latitude and longitude for a location
    
    Args:
        location: Location name
        
    Returns:
        Dict with 'lat' and 'lng' or None if not found
    """
    try:
        # Run in executor to avoid blocking
        loop = asyncio.get_event_loop()
        location_data = await loop.run_in_executor(
            None, 
            geolocator.geocode, 
            location
        )
        
        if location_data:
            return {
                "lat": location_data.latitude,
                "lng": location_data.longitude
            }
    except Exception as e:
        print(f"Error geocoding {location}: {e}")
    
    return None


def calculate_distance(coord1: Dict[str, float], coord2: Dict[str, float]) -> float:
    """
    Calculate distance between two coordinates in kilometers
    
    Args:
        coord1: First coordinate dict with 'lat' and 'lng'
        coord2: Second coordinate dict with 'lat' and 'lng'
        
    Returns:
        Distance in kilometers
    """
    point1 = (coord1["lat"], coord1["lng"])
    point2 = (coord2["lat"], coord2["lng"])
    return geodesic(point1, point2).kilometers


async def optimize_route(destinations: List[str]) -> List[str]:
    """
    Optimize the order of destinations to minimize travel distance
    Uses a simple nearest-neighbor algorithm
    
    Args:
        destinations: List of destination names
        
    Returns:
        Optimized list of destination names
    """
    if len(destinations) <= 2:
        return destinations
    
    # Get coordinates for all destinations
    coords = {}
    for dest in destinations:
        coord = await get_coordinates(dest)
        if coord:
            coords[dest] = coord
    
    if len(coords) < 2:
        return destinations
    
    # Nearest neighbor algorithm
    optimized = [destinations[0]]
    remaining = set(destinations[1:])
    
    while remaining:
        current = optimized[-1]
        if current not in coords:
            # If we can't geocode current, just add next remaining
            optimized.append(remaining.pop())
            continue
            
        # Find nearest destination
        nearest = None
        min_distance = float('inf')
        
        for dest in remaining:
            if dest in coords:
                dist = calculate_distance(coords[current], coords[dest])
                if dist < min_distance:
                    min_distance = dist
                    nearest = dest
        
        if nearest:
            optimized.append(nearest)
            remaining.remove(nearest)
        else:
            # If no geocoded destination found, just add any
            optimized.append(remaining.pop())
    
    return optimized


async def calculate_route_info(destinations: List[str]) -> Dict:
    """
    Calculate total distance and estimated travel times
    
    Args:
        destinations: Ordered list of destinations
        
    Returns:
        Dict with route information
    """
    if len(destinations) < 2:
        return {
            "total_distance_km": 0,
            "segments": []
        }
    
    coords = {}
    for dest in destinations:
        coord = await get_coordinates(dest)
        if coord:
            coords[dest] = coord
    
    segments = []
    total_distance = 0
    
    for i in range(len(destinations) - 1):
        from_dest = destinations[i]
        to_dest = destinations[i + 1]
        
        if from_dest in coords and to_dest in coords:
            distance = calculate_distance(coords[from_dest], coords[to_dest])
            # Rough estimate: 60 km/h average travel speed
            travel_hours = distance / 60
            
            segments.append({
                "from": from_dest,
                "to": to_dest,
                "distance_km": round(distance, 1),
                "estimated_hours": round(travel_hours, 1)
            })
            
            total_distance += distance
    
    return {
        "total_distance_km": round(total_distance, 1),
        "segments": segments
    }


def calculate_days_per_destination(
    destinations: List[str], 
    total_days: int
) -> Dict[str, int]:
    """
    Distribute days across destinations
    
    Args:
        destinations: List of destination names
        total_days: Total trip duration in days
        
    Returns:
        Dict mapping destination to number of days
    """
    num_destinations = len(destinations)
    
    if num_destinations == 0:
        return {}
    
    # Base allocation
    days_per_dest = total_days // num_destinations
    extra_days = total_days % num_destinations
    
    allocation = {}
    for i, dest in enumerate(destinations):
        # Give extra days to first destinations
        allocation[dest] = days_per_dest + (1 if i < extra_days else 0)
    
    return allocation
