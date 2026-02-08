"""
Validation module - Input validation, error handling, and data quality checks
Prevents crashes and handles edge cases gracefully
"""

import logging
from typing import Tuple, Optional, Dict, List
import config

# Setup logging
logger = logging.getLogger("CoastGuard.Validation")

class ValidationError(Exception):
    """Custom exception for validation failures"""
    pass

class CoordinateValidator:
    """Validates geographic coordinates"""
    
    @staticmethod
    def validate_lat(lat: float) -> bool:
        """Check if latitude is valid"""
        if not isinstance(lat, (int, float)):
            raise ValidationError(f"Latitude must be numeric, got {type(lat)}")
        if not (config.LAT_MIN <= lat <= config.LAT_MAX):
            raise ValidationError(f"Latitude {lat} outside Kerala bounds ({config.LAT_MIN}-{config.LAT_MAX})")
        return True
    
    @staticmethod
    def validate_lon(lon: float) -> bool:
        """Check if longitude is valid"""
        if not isinstance(lon, (int, float)):
            raise ValidationError(f"Longitude must be numeric, got {type(lon)}")
        if not (config.LON_MIN <= lon <= config.LON_MAX):
            raise ValidationError(f"Longitude {lon} outside Kerala bounds ({config.LON_MIN}-{config.LON_MAX})")
        return True
    
    @staticmethod
    def validate_coordinates(lat: float, lon: float) -> Tuple[bool, Optional[str]]:
        """Validate lat/lon pair, return (is_valid, error_message)"""
        try:
            CoordinateValidator.validate_lat(lat)
            CoordinateValidator.validate_lon(lon)
            return True, None
        except ValidationError as e:
            error_msg = str(e)
            logger.warning(f"Invalid coordinates: {error_msg}")
            return False, error_msg

class RiskValidator:
    """Validates risk assessment parameters"""
    
    @staticmethod
    def validate_mangrove_width(width: float) -> Tuple[bool, Optional[str]]:
        """Validate mangrove width (0-300 meters reasonable)"""
        try:
            if not isinstance(width, (int, float)):
                raise ValidationError(f"Width must be numeric, got {type(width)}")
            if width < 0 or width > 300:
                raise ValidationError(f"Mangrove width {width}m seems unrealistic (0-300m expected)")
            return True, None
        except ValidationError as e:
            logger.warning(str(e))
            return False, str(e)
    
    @staticmethod
    def validate_salinity(salinity: int) -> Tuple[bool, Optional[str]]:
        """Validate salinity (0-40000 ppm)"""
        try:
            if not isinstance(salinity, (int, float)):
                raise ValidationError(f"Salinity must be numeric, got {type(salinity)}")
            if salinity < 0 or salinity > 40000:
                raise ValidationError(f"Salinity {salinity}ppm outside realistic range (0-40000)")
            return True, None
        except ValidationError as e:
            logger.warning(str(e))
            return False, str(e)
    
    @staticmethod
    def validate_sea_state(state: str) -> Tuple[bool, Optional[str]]:
        """Validate sea state observation"""
        valid_states = ["Calm", "Choppy", "Rough"]
        if state not in valid_states:
            error = f"Sea state '{state}' invalid. Must be one of: {valid_states}"
            logger.warning(error)
            return False, error
        return True, None

class ShelterValidator:
    """Validates shelter data integrity"""
    
    @staticmethod
    def validate_shelter(shelter: Dict) -> Tuple[bool, Optional[str]]:
        """Check if shelter has all required fields"""
        required_fields = ["id", "name", "lat", "lon", "capacity"]
        missing = [f for f in required_fields if f not in shelter]
        if missing:
            error = f"Shelter missing fields: {missing}"
            logger.error(error)
            return False, error
        
        # Validate coordinates
        is_valid, msg = CoordinateValidator.validate_coordinates(shelter["lat"], shelter["lon"])
        if not is_valid:
            logger.error(f"Shelter {shelter['id']} has invalid coordinates: {msg}")
            return False, msg
        
        # Validate capacity
        if not isinstance(shelter["capacity"], int) or shelter["capacity"] <= 0:
            error = f"Shelter capacity must be positive integer, got {shelter['capacity']}"
            logger.error(error)
            return False, error
        
        return True, None

class DistanceValidator:
    """Validates distance calculations"""
    
    @staticmethod
    def validate_distance(distance_m: float) -> Tuple[bool, Optional[str]]:
        """Check if distance is reasonable"""
        if distance_m < 0:
            error = f"Distance cannot be negative: {distance_m}m"
            logger.warning(error)
            return False, error
        if distance_m > 100000:  # >100km is unrealistic for evacuations
            error = f"Distance {distance_m}m seems unrealistic for local evacuation"
            logger.warning(error)
            return False, error
        return True, None

class EvacuationTimeCalculator:
    """Calculate realistic evacuation times"""
    
    @staticmethod
    def calculate_evacuation_time(distance_m: float) -> Dict:
        """
        Calculate evacuation time with realistic assumptions
        
        Returns dict with:
        - time_min: evacuation time in minutes
        - time_with_delay: total time including reaction delay
        - speed_assumption: walking speed used (m/s)
        """
        is_valid, msg = DistanceValidator.validate_distance(distance_m)
        if not is_valid:
            logger.error(f"Invalid distance for evacuation calculation: {msg}")
            return {
                "time_min": 0,
                "time_with_delay": 0,
                "speed_assumption": config.EVACUATION_SPEED_MS,
                "error": msg
            }
        
        time_seconds = distance_m / config.EVACUATION_SPEED_MS
        time_minutes = time_seconds / 60
        total_with_delay = time_minutes + config.EVACUATION_DELAY_MIN
        
        return {
            "distance_m": distance_m,
            "distance_km": round(distance_m / 1000, 2),
            "time_min": round(time_minutes, 1),
            "time_with_delay": round(total_with_delay, 1),
            "speed_assumption": f"{config.EVACUATION_SPEED_MS} m/s (walking)",
            "reaction_delay_min": config.EVACUATION_DELAY_MIN,
            "description": f"~{int(total_with_delay)} minutes to evacuate (includes {config.EVACUATION_DELAY_MIN}min reaction time)"
        }

def validate_all_inputs(lat: float, lon: float, width: float, salinity: int, sea_state: str) -> Tuple[bool, List[str]]:
    """
    Validate all user inputs at once
    
    Returns:
        (is_all_valid, list_of_errors)
    """
    errors = []
    
    # Validate coordinates
    coord_valid, coord_err = CoordinateValidator.validate_coordinates(lat, lon)
    if not coord_valid:
        errors.append(f"Location: {coord_err}")
    
    # Validate width
    width_valid, width_err = RiskValidator.validate_mangrove_width(width)
    if not width_valid:
        errors.append(f"Mangrove Width: {width_err}")
    
    # Validate salinity
    salinity_valid, salinity_err = RiskValidator.validate_salinity(salinity)
    if not salinity_valid:
        errors.append(f"Salinity: {salinity_err}")
    
    # Validate sea state
    sea_valid, sea_err = RiskValidator.validate_sea_state(sea_state)
    if not sea_valid:
        errors.append(f"Sea State: {sea_err}")
    
    return len(errors) == 0, errors
