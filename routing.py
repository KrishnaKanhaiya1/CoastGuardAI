"""
Evacuation Routing Module - Shortest path to shelters with time estimates
Includes distance calculation, route generation, and evacuation time prediction
"""

import math
import logging
from typing import List, Tuple, Dict, Optional
from validation import DistanceValidator, EvacuationTimeCalculator, ValidationError

logger = logging.getLogger("CoastGuard.Routing")

def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """
    Calculate great-circle distance between two points (haversine formula)
    
    Args:
        lon1, lat1: Starting point (longitude, latitude)
        lon2, lat2: Ending point (longitude, latitude)
    
    Returns:
        Distance in meters
    """
    try:
        R = 6371000  # Earth radius in meters
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
        return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))
    except (TypeError, ValueError) as e:
        logger.error(f"Haversine calculation failed: {e}")
        return float('inf')

def is_in_water(lon: float, lat: float) -> bool:
    """
    Basic water detection for Kochi region
    (Real system would use proper GIS water boundaries)
    
    Returns True if point appears to be in water
    """
    # Rough approximation: Arabian Sea area near Kochi
    # Longitude < 76.1 is generally water
    if lon < 76.1:
        logger.info(f"Coordinate ({lat}, {lon}) detected as water body")
        return True
    return False

def nearest_shelter(user_lon: float, user_lat: float, shelters: List[Dict]) -> Tuple[Optional[Dict], float]:
    """
    Find nearest verified shelter using haversine distance
    
    Args:
        user_lon, user_lat: User location
        shelters: List of shelter dictionaries with 'lon', 'lat' keys
    
    Returns:
        (shelter_dict, distance_in_meters) or (None, inf) if no shelters available
    """
    if not shelters:
        logger.error("No shelters available")
        return None, float('inf')
    
    best_shelter = None
    best_distance = float('inf')
    
    for shelter in shelters:
        try:
            d = haversine(user_lon, user_lat, shelter['lon'], shelter['lat'])
            if d < best_distance:
                best_distance = d
                best_shelter = shelter
        except (KeyError, TypeError) as e:
            logger.warning(f"Error processing shelter {shelter}: {e}")
            continue
    
    if best_shelter:
        logger.info(f"Found nearest shelter: {best_shelter['name']} at {best_distance:.0f}m")
    
    return best_shelter, best_distance

def simple_route(start_lon: float, start_lat: float, end_lon: float, end_lat: float, steps: int = 10) -> List[Dict]:
    """
    Generate simple straight-line route between two points
    
    WARNING: This is a DEMO route. Real evacuation routing should:
    - Use actual street networks
    - Avoid obstacles (buildings, water bodies)
    - Consider traffic patterns
    - Calculate actual travel time
    
    Args:
        start_lon, start_lat: Starting point
        end_lon, end_lat: Destination (shelter)
        steps: Number of waypoints (default 10)
    
    Returns:
        List of waypoints with lon/lat
    """
    route = []
    
    # Check if start or end is in water (basic warning)
    if is_in_water(start_lon, start_lat):
        logger.warning(f"Route starts in water body: ({start_lat}, {start_lon})")
    if is_in_water(end_lon, end_lat):
        logger.warning(f"Route ends in water body: ({end_lat}, {end_lon})")
    
    for i in range(steps + 1):
        t = i / steps  # interpolation parameter (0 to 1)
        lon = start_lon + (end_lon - start_lon) * t
        lat = start_lat + (end_lat - start_lat) * t
        route.append({'lon': lon, 'lat': lat, 'step': i})
    
    logger.info(f"Route generated with {len(route)} waypoints")
    return route

def get_evacuation_plan(user_lon: float, user_lat: float, nearest_shelter: Dict) -> Dict:
    """
    Generate complete evacuation plan with time estimates
    
    Returns dict with:
    - distance
    - time_to_shelter
    - time_with_reaction
    - shelter_info
    - waypoints
    """
    distance = haversine(user_lon, user_lat, nearest_shelter['lon'], nearest_shelter['lat'])
    
    # Validate distance
    is_valid, msg = DistanceValidator.validate_distance(distance)
    if not is_valid:
        logger.error(f"Invalid evacuation distance: {msg}")
        return {"error": msg}
    
    # Calculate evacuation time
    time_calc = EvacuationTimeCalculator.calculate_evacuation_time(distance)
    
    # Generate route waypoints
    route = simple_route(user_lon, user_lat, nearest_shelter['lon'], nearest_shelter['lat'])
    
    return {
        "shelter": nearest_shelter['name'],
        "shelter_id": nearest_shelter['id'],
        "shelter_capacity": nearest_shelter['capacity'],
        "distance_m": round(distance, 0),
        "distance_km": round(distance / 1000, 2),
        "evacuation_time_min": time_calc['time_min'],
        "total_time_with_reaction_min": time_calc['time_with_delay'],
        "description": time_calc['description'],
        "route_waypoints": route,
        "coordinates": {
            "user": {"lon": user_lon, "lat": user_lat},
            "shelter": {"lon": nearest_shelter['lon'], "lat": nearest_shelter['lat']}
        }
    }

