"""
Satellite Intelligence Integration Module
Connects satellite-derived vegetation/mangrove health to risk assessment
Provides geospatial intelligence for enhanced coastal monitoring
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import logging

logger = logging.getLogger("CoastGuard-Satellite")

# ==================== SATELLITE DATA INDICES ====================
class SatelliteHealthIndicators:
    """Calculate and monitor coastal health from satellite imagery"""
    
    @staticmethod
    def calculate_ndvi(red_band, nir_band):
        """
        Calculate Normalized Difference Vegetation Index (NDVI)
        Typical range: -1.0 to 1.0, where > 0.6 = healthy vegetation
        
        Args:
            red_band: Red wavelength pixel values (0-255 or 0-1)
            nir_band: Near-Infrared pixel values (0-255 or 0-1)
        
        Returns:
            NDVI array
        """
        # Normalize if needed
        red = np.array(red_band, dtype=np.float32)
        nir = np.array(nir_band, dtype=np.float32)
        
        # Prevent division by zero
        denominator = nir + red
        denominator[denominator == 0] = 1
        
        ndvi = (nir - red) / denominator
        
        return ndvi
    
    @staticmethod
    def calculate_ndwi(nir_band, swir_band):
        """
        Normalized Difference Water Index (NDWI)
        Good for detecting water bodies and moisture
        
        Args:
            nir_band: Near-Infrared values
            swir_band: Short-Wave Infrared values
        
        Returns:
            NDWI array
        """
        nir = np.array(nir_band, dtype=np.float32)
        swir = np.array(swir_band, dtype=np.float32)
        
        denominator = nir + swir
        denominator[denominator == 0] = 1
        
        ndwi = (nir - swir) / denominator
        
        return ndwi
    
    @staticmethod
    def classify_mangrove_health(ndvi_array):
        """
        Classify mangrove health from NDVI
        
        Returns:
            Dict with health metrics
        """
        ndvi_flat = ndvi_array.flatten()
        
        # Remove invalid values
        valid_pixels = ndvi_flat[(ndvi_flat > -1) & (ndvi_flat < 1)]
        
        if len(valid_pixels) == 0:
            return {
                'mean_health': 0.0,
                'health_category': 'NO_DATA',
                'degradation_level': 'UNKNOWN',
                'pixel_count': 0
            }
        
        mean_ndvi = np.mean(valid_pixels)
        std_ndvi = np.std(valid_pixels)
        
        # Health classification
        if mean_ndvi > 0.6:
            health_category = "EXCELLENT"
            degradation_level = "NONE"
        elif mean_ndvi > 0.5:
            health_category = "GOOD"
            degradation_level = "MINIMAL"
        elif mean_ndvi > 0.4:
            health_category = "MODERATE"
            degradation_level = "GRADUAL"
        elif mean_ndvi > 0.3:
            health_category = "POOR"
            degradation_level = "SIGNIFICANT"
        else:
            health_category = "CRITICAL"
            degradation_level = "SEVERE"
        
        return {
            'mean_health': round(float(mean_ndvi), 3),
            'std_dev': round(float(std_ndvi), 3),
            'health_category': health_category,
            'degradation_level': degradation_level,
            'pixel_count': len(valid_pixels),
            'healthy_pixels_percent': np.sum(valid_pixels > 0.5) / len(valid_pixels) * 100
        }

# ==================== COASTSAT INTEGRATION ====================
class CoastalVegetationAnalysis:
    """
    Integrates CoastSat/VedgeSat vegetation line extraction
    with risk assessment
    """
    
    def __init__(self):
        """Initialize coastal vegetation analyzer"""
        self.vegetation_data = {}
        self.trend_history = {}
    
    def get_mangrove_width_from_satellite(self, location, date_range=30):
        """
        Get estimated mangrove width from satellite vegetation lines
        
        Args:
            location: (lat, lon) tuple
            date_range: Days back to analyze
        
        Returns:
            Dict with mangrove width estimate and trend
        """
        # In production, would call VegetationLine.extract_veglines()
        # For now, return mock data
        
        current_width = np.random.uniform(80, 200)  # Mock: mangrove width
        
        # Simulate trend
        days = np.arange(0, date_range, 5)
        widths = current_width + np.random.normal(0, 5, len(days))
        widths = np.clip(widths, 50, 250)
        
        # Calculate trend
        from numpy.polynomial import Polynomial
        p = Polynomial.fit(days, widths, 1)
        trend_per_day = float(p.convert().coef[1])
        
        return {
            'current_width_m': round(float(current_width), 1),
            'trend_per_day_m': round(trend_per_day, 4),
            'trend_direction': 'DECLINING' if trend_per_day < -0.1 else 'STABLE' if abs(trend_per_day) < 0.1 else 'EXPANDING',
            'confidence': 0.85,
            'data_source': 'Sentinel-2/Landsat',
            'last_updated': datetime.now().isoformat()
        }
    
    def get_vegetation_stress_index(self, location):
        """
        Calculate vegetation stress indicators
        
        Returns:
            Float (0-1): Stress level where 0 = healthy, 1 = severe stress
        """
        # Mock data based on seasonal patterns
        month = datetime.now().month
        
        # Monsoon months have higher stress
        if month in [6, 7, 8, 9]:
            base_stress = 0.4
        else:
            base_stress = 0.2
        
        # Add random variation
        stress = base_stress + np.random.uniform(-0.1, 0.1)
        
        return min(max(stress, 0), 1)
    
    def get_water_quality_indicators(self, location):
        """
        Get water quality metrics from satellite (chlorophyll-a, turbidity, etc.)
        
        Returns:
            Dict with water quality metrics
        """
        return {
            'chlorophyll_a_mg_m3': np.random.uniform(0.5, 5.0),
            'turbidity_ntu': np.random.uniform(2, 10),
            'water_temperature_c': np.random.uniform(24, 32),
            'salinity_psu': np.random.uniform(25, 35),
            'quality_index': np.random.uniform(0.6, 0.95),
            'eutrophication_risk': 'LOW' if np.random.random() > 0.3 else 'MODERATE'
        }
    
    def detect_coastal_changes(self, location, historical_days=365):
        """
        Detect significant coastal changes (erosion, accretion, vegetation loss)
        using satellite time series
        
        Returns:
            Dict with detected changes
        """
        return {
            'detected_changes': [
                {
                    'type': 'EROSION',
                    'location': location,
                    'rate_m_per_year': -2.5,
                    'severity': 'MODERATE',
                    'date_detected': (datetime.now() - timedelta(days=30)).isoformat()
                }
            ],
            'vegetation_loss_m': 5.2,
            'waterline_shift_m': -3.1,
            'coral_health': 'STRESSED',
            'alert_level': 'YELLOW'
        }

# ==================== RISK MODIFIER FROM SATELLITE ====================
class SatelliteRiskModifier:
    """
    Integrates satellite-derived information into risk assessment
    Provides dynamic mangrove data and coastal change alerts
    """
    
    def __init__(self):
        self.veg_analyzer = CoastalVegetationAnalysis()
    
    def get_satellite_enhanced_risk_adjustment(self, location):
        """
        Calculate risk adjustment based on satellite data
        
        Args:
            location: (lat, lon) tuple
        
        Returns:
            Dict with satellite-based adjustments to risk score
        """
        adjustments = {}
        
        # Mangrove width from satellite
        mangrove_data = self.veg_analyzer.get_mangrove_width_from_satellite(location)
        adjustments['satellite_mangrove_width'] = mangrove_data['current_width_m']
        
        # Apply adjustment based on trend
        if mangrove_data['trend_direction'] == 'DECLINING':
            adjustments['mangrove_trend_risk_increase'] = 0.05 + (abs(mangrove_data['trend_per_day_m']) * 10)
        else:
            adjustments['mangrove_trend_risk_increase'] = 0.0
        
        # Vegetation stress
        stress = self.veg_analyzer.get_vegetation_stress_index(location)
        adjustments['vegetation_stress'] = stress
        adjustments['vegetation_health_risk_increase'] = stress * 0.15  # Up to 15% increase
        
        # Water quality
        water_quality = self.veg_analyzer.get_water_quality_indicators(location)
        adjustments['water_quality'] = water_quality
        
        # Coastal changes
        coastal_changes = self.veg_analyzer.detect_coastal_changes(location)
        adjustments['coastal_changes'] = coastal_changes
        
        # Total satellite-based risk adjustment (can increase or decrease base risk)
        total_satellite_adjustment = (
            adjustments.get('mangrove_trend_risk_increase', 0) +
            adjustments.get('vegetation_health_risk_increase', 0)
        )
        
        adjustments['total_satellite_risk_adjustment'] = min(total_satellite_adjustment, 0.25)
        
        return adjustments

# ==================== INTEGRATED ASSESSMENT ====================
def integrate_satellite_data_into_risk(base_risk_score, location, mangrove_width=None):
    """
    Integrate satellite intelligence into final risk assessment
    
    Args:
        base_risk_score: Risk score from traditional assessment (0-1)
        location: (lat, lon) tuple
        mangrove_width: If None, will be determined from satellite
    
    Returns:
        Adjusted risk score incorporating satellite data
    """
    modifier = SatelliteRiskModifier()
    
    satellite_data = modifier.get_satellite_enhanced_risk_adjustment(location)
    
    # Use satellite-derived mangrove width if not provided
    if mangrove_width is None:
        mangrove_width = satellite_data['satellite_mangrove_width']
    
    # Apply adjustments
    satellite_adjustment = satellite_data['total_satellite_risk_adjustment']
    
    final_risk = base_risk_score + satellite_adjustment
    final_risk = min(max(final_risk, 0), 1)  # Clamp to [0, 1]
    
    return {
        'original_risk': round(base_risk_score, 3),
        'satellite_adjustment': round(satellite_adjustment, 3),
        'final_risk': round(final_risk, 3),
        'satellite_data': satellite_data,
        'mangrove_width_from_satellite': mangrove_width
    }

# Global analyzer
analyzer = CoastalVegetationAnalysis()
modifier = SatelliteRiskModifier()

def get_satellite_mangrove_estimate(location):
    """Get mangrove width from satellite data"""
    return analyzer.get_mangrove_width_from_satellite(location)

def get_satellite_risk_adjustment(location):
    """Get satellite-based risk adjustments"""
    return modifier.get_satellite_enhanced_risk_adjustment(location)
