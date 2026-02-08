"""
Enhanced Cyclone Tracking Module
Combines synthetic data with ML-predicted tracks and real cyclone forecasts
"""

import math
import numpy as np
from datetime import datetime

# Try to import ML predictor
try:
    from ml_cyclone_predictor import predict_cyclone_track_ml, get_landfall_risk
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

def generate_cone(track_points, max_width_km=30, steps=20):
    """
    Generate a realistic 'Cone of Uncertainty' polygon
    Uses increasing uncertainty with forecast lead time
    
    Args:
        track_points: list of (lon, lat)
        max_width_km: Maximum cone width at forecast end
        steps: Number of points per circle
    
    Returns:
        List of polygons (each as list of [lat, lon]) for display
    """
    if not track_points:
        return []

    cone_polygons = []
    
    for i, (lon, lat) in enumerate(track_points):
        # Uncertainty grows with time/distance (approximately 20 km/day)
        progression = (i + 1) / len(track_points)
        radius_km = 5 + (max_width_km * progression)
        
        ring = []
        for a in range(steps + 1):  # Close the loop
            angle = 2 * math.pi * a / steps
            
            # Convert km to degrees (roughly 1 degree = 111 km)
            dlat = (radius_km / 111.32) * math.cos(angle)
            dlon = (radius_km / (111.32 * math.cos(math.radians(lat)))) * math.sin(angle)
            
            ring.append([lat + dlat, lon + dlon])
        
        cone_polygons.append(ring)
        
    return cone_polygons

def sample_synthetic_track(center_lon=76.22, center_lat=10.0, length=5, spacing_km=50):
    """
    Generate a synthetic cyclone track for testing
    Moves from offshore towards Indian coast
    
    Args:
        center_lon: Starting longitude (offshore)
        center_lat: Starting latitude
        length: Number of track points
        spacing_km: Approximate spacing between points
    
    Returns:
        List of (lon, lat) tuples
    """
    pts = []
    # Start slightly offshore (South-West) moving North-East
    start_lon = center_lon - 0.5
    start_lat = center_lat - 0.5
    
    for i in range(length):
        lon = start_lon + (i * 0.1)
        lat = start_lat + (i * 0.12)
        pts.append((lon, lat))
    
    return pts

def get_ml_predicted_track(current_lon=75.5, current_lat=10.5, 
                           current_pressure=990, current_wind=80, hours=120):
    """
    Get ML-predicted cyclone track if available
    Falls back to synthetic if ML unavailable
    
    Args:
        current_lon, current_lat: Current cyclone center
        current_pressure: Current central pressure (mb)
        current_wind: Current max wind speed (km/h)
        hours: Forecast period in hours
    
    Returns:
        Track points as list of (lon, lat) tuples
    """
    if not ML_AVAILABLE:
        return sample_synthetic_track()
    
    try:
        prediction = predict_cyclone_track_ml(
            current_lon=current_lon,
            current_lat=current_lat,
            current_pressure=current_pressure,
            current_wind=current_wind,
            hours=hours
        )
        
        if prediction and 'track_points' in prediction:
            return prediction['track_points']
    
    except Exception as e:
        print(f"ML prediction failed, using synthetic: {e}")
    
    return sample_synthetic_track(current_lon, current_lat)

def get_cyclone_landfall_probability(track_points, region=None):
    """
    Calculate cyclone landfall probability
    
    Args:
        track_points: List of (lon, lat) tuples
        region: {'min_lon', 'max_lon', 'min_lat', 'max_lat'} or None for default Kerala
    
    Returns:
        Float (0-1): Probability of landfall
    """
    if region is None:
        # Default: Kerala coast region
        region = {
            'min_lon': 75.0,
            'max_lon': 77.5,
            'min_lat': 8.5,
            'max_lat': 12.5
        }
    
    if ML_AVAILABLE and len(track_points) > 0:
        try:
            return get_landfall_risk(track_points, 
                                    region['min_lon'], region['max_lon'],
                                    region['min_lat'], region['max_lat'])
        except Exception:
            pass
    
    # Fallback: Simple calculation
    if not track_points:
        return 0.0
    
    landfall_points = [
        p for p in track_points
        if (region['min_lon'] <= p[0] <= region['max_lon'] and
            region['min_lat'] <= p[1] <= region['max_lat'])
    ]
    
    return len(landfall_points) / len(track_points) if track_points else 0.0

