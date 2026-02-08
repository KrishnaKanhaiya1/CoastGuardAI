import pandas as pd

def calculate_hybrid_risk(mangrove_width, sea_state, wind_speed, tide_level=0, rainfall_mm=0):
    """
    Fuses Satellite (Mangrove) and Indigenous (Fishermen) data.
    Includes real-time environmental factors: tide level and rainfall.
    """
    # 1. BASE SATELLITE RISK (Roadmap suggests 0.3 as a baseline)
    satellite_flood_risk = 0.3
    
    # 2. QUANTIFY INDIGENOUS WISDOM (Logic from Roadmap)
    # Mapping dashboard selections to the roadmap's risk weights
    indigenous_score = 0
    if sea_state == "Rough": # Equivalent to 'Anomalous Swell'
        indigenous_score += 0.4 
    elif sea_state == "Choppy":
        indigenous_score += 0.2
        
    if wind_speed == "Very High": # Equivalent to 'Cyclonic'
        indigenous_score += 0.2
    elif wind_speed == "High":
        indigenous_score += 0.1
        
    # 3. REAL-TIME ENVIRONMENTAL FACTORS
    # Tide contribution: higher tide = more risk (normalized to 0-0.2)
    tide_contribution = min((tide_level / 3.0) * 0.2, 0.2)
    
    # Rainfall contribution: higher rainfall = more risk (normalized to 0-0.15)
    rainfall_contribution = min((rainfall_mm / 500.0) * 0.15, 0.15)
    
    # 4. BIOSHIELD BUFFERING (The "Mangrove Effect")
    # Protection factor capped at 0.5 as per roadmap rules
    protection_factor = min(mangrove_width / 100, 0.5)
    
    # 5. THE FUSION FORMULA (From Roadmap)
    # Final Risk = Base + Traditional Warning + Environmental Factors - Nature's Protection
    final_risk = satellite_flood_risk + indigenous_score + tide_contribution + rainfall_contribution - protection_factor
    
    # Normalize result between 0.0 (Safe) and 1.0 (Critical)
    return round(max(0.0, min(1.0, final_risk)), 2)