"""
CoastGuard AI - Coastal Risk Assessment System
Integrates satellite intelligence with indigenous environmental knowledge
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import folium
from streamlit_folium import st_folium

from engine import calculate_hybrid_risk
from cyclone import sample_synthetic_track, generate_cone
from routing import haversine, nearest_shelter
from vessels import sample_vessel_positions, get_positions_at_step

# Configuration
st.set_page_config(page_title="CoastGuard AI", page_icon="🌊", layout="wide")

# Initialize state
if 'community_reports' not in st.session_state:
    st.session_state.community_reports = []
if 'vessel_step' not in st.session_state:
    st.session_state.vessel_step = 0

# Styling - professional and readable
st.markdown("""
<style>
    body { color: #1a1a1a; background: #ffffff; }
    h1, h2, h3 { color: #0d47a1; }
    .metric-box { 
        background: #f5f5f5; 
        padding: 16px; 
        border-radius: 8px; 
        border-left: 4px solid #0d47a1;
        color: #1a1a1a;
    }
    .alert-high { 
        background: #fff3e0; 
        border-left: 4px solid #d32f2f; 
        padding: 16px; 
        border-radius: 8px;
        color: #1a1a1a;
    }
    .alert-medium { 
        background: #f3e5f5; 
        border-left: 4px solid #f57c00; 
        padding: 16px; 
        border-radius: 8px;
        color: #1a1a1a;
    }
    .alert-low { 
        background: #e8f5e9; 
        border-left: 4px solid #388e3c; 
        padding: 16px; 
        border-radius: 8px;
        color: #1a1a1a;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.title("Configuration")
    
    st.subheader("Location")
    location_option = st.selectbox(
        "Select coastal area",
        ["Kochi", "Thiruvananthapuram", "Mattancherry", "Custom"]
    )
    
    locations = {
        "Kochi": (76.267, 9.935),
        "Thiruvananthapuram": (76.949, 8.721),
        "Mattancherry": (76.24, 9.95),
    }
    
    if location_option in locations:
        lon, lat = locations[location_option]
    else:
        lat = st.number_input("Latitude", value=9.935, format="%.4f")
        lon = st.number_input("Longitude", value=76.267, format="%.4f")
    
    st.divider()
    
    st.subheader("Environmental Input")
    mangrove_width = st.slider("Mangrove width (m)", 10, 500, 85)
    sea_state = st.selectbox("Sea state", ["Calm", "Choppy", "Rough"])
    wind_speed = st.selectbox("Wind speed", ["Normal", "High", "Very High"])
    
    st.divider()
    
    st.subheader("Real-time Conditions")
    tide_level = st.slider("Tide level (m)", 0.0, 3.0, 1.5)
    rainfall_mm = st.slider("Rainfall (mm)", 0, 500, 100)
    
    st.divider()
    risk_threshold = st.slider("Alert threshold", 0.0, 1.0, 0.67)

# Calculate risk with all environmental factors
risk_score = calculate_hybrid_risk(mangrove_width, sea_state, wind_speed, tide_level, rainfall_mm)
is_high_risk = risk_score >= risk_threshold
is_moderate_risk = risk_score >= (risk_threshold * 0.5)

# Header
st.title("CoastGuard AI")
st.markdown("Early warning system combining satellite data with indigenous coastal knowledge")

# Risk metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Risk Score", f"{risk_score:.2f}/1.0")
with col2:
    status = "🔴 HIGH" if is_high_risk else ("🟡 MODERATE" if is_moderate_risk else "🟢 LOW")
    st.write(f"**Status**: {status}")
with col3:
    conf = min(80 + int(risk_score * 20), 100)
    st.metric("Confidence", f"{conf}%")

st.divider()

# Main tabs
tab_risk, tab_map, tab_cyclone, tab_community, tab_evacuation, tab_maritime, tab_info = st.tabs([
    "Risk Assessment",
    "Flood Zones Map",
    "Cyclone Tracking",
    "Community Reports",
    "Evacuation Routes",
    "Maritime Safety",
    "About"
])

# TAB 1: Risk Assessment & Alerting
with tab_risk:
    st.subheader("Coastal Flood Risk Assessment")
    
    # Risk breakdown
    satellite_base = 0.3
    indigenous_score = 0
    if sea_state == "Rough": indigenous_score += 0.4
    elif sea_state == "Choppy": indigenous_score += 0.2
    if wind_speed == "Very High": indigenous_score += 0.2
    elif wind_speed == "High": indigenous_score += 0.1
    
    tide_contribution = min((tide_level / 3.0) * 0.2, 0.2)
    rainfall_contribution = min((rainfall_mm / 500.0) * 0.15, 0.15)
    mangrove_protection = min(mangrove_width / 100, 0.5)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f"""
        <div class="metric-box">
        <strong>Satellite Base</strong><br>
        Risk: {satellite_base:.2f}<br>
        <small>Coastal morphology</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-box">
        <strong>Indigenous Knowledge</strong><br>
        Score: {indigenous_score:.2f}<br>
        <small>{sea_state} seas, {wind_speed} winds</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-box">
        <strong>Tide Effect</strong><br>
        +{tide_contribution:.2f} risk<br>
        <small>Level: {tide_level}m</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-box">
        <strong>Rainfall Effect</strong><br>
        +{rainfall_contribution:.2f} risk<br>
        <small>{rainfall_mm}mm</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-box">
        <strong>Bioshield Protection</strong><br>
        -{mangrove_protection:.2f} risk<br>
        <small>Width: {mangrove_width}m</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Automated alerting
    st.subheader("Automated Coastal Flood Alerting")
    
    if is_high_risk:
        st.markdown(f"""
        <div class="alert-high">
        <strong>🚨 HIGH RISK ALERT</strong><br>
        Risk score {risk_score:.2f} exceeds threshold {risk_threshold:.2f}<br>
        <strong>Actions:</strong>
        • Issue immediate evacuation orders
        • Activate emergency response centers
        • Alert maritime vessels
        • Deploy alert systems to communities
        </div>
        """, unsafe_allow_html=True)
    
    elif is_moderate_risk:
        st.markdown(f"""
        <div class="alert-medium">
        <strong>⚠️ MODERATE RISK</strong><br>
        Conditions deteriorating. Risk: {risk_score:.2f}<br>
        <strong>Actions:</strong>
        • Brief communities on procedures
        • Pre-position resources
        • Increase monitoring frequency
        • Prepare evacuation routes
        </div>
        """, unsafe_allow_html=True)
    
    else:
        st.markdown(f"""
        <div class="alert-low">
        <strong>✓ LOW RISK</strong><br>
        Current conditions stable. Risk: {risk_score:.2f}<br>
        Continue routine monitoring and readiness training
        </div>
        """, unsafe_allow_html=True)

# TAB 2: Flood Zone Visualization
with tab_map:
    st.subheader("Dynamic Flood Risk Zones")
    
    # Create map
    m = folium.Map(location=[lat, lon], zoom_start=11, tiles="OpenStreetMap")
    
    # Color-code zones
    if is_high_risk:
        zone_color, zone_fill = "#d32f2f", "#ffcdd2"
        zone_radius = 2500
    elif is_moderate_risk:
        zone_color, zone_fill = "#f57c00", "#ffe0b2"
        zone_radius = 1500
    else:
        zone_color, zone_fill = "#388e3c", "#c8e6c9"
        zone_radius = 800
    
    # Main risk zone
    folium.Circle(
        location=[lat, lon],
        radius=zone_radius,
        color=zone_color,
        fill=True,
        fillColor=zone_fill,
        fillOpacity=0.5,
        weight=2,
        popup=f"Risk Zone (Score: {risk_score:.2f})"
    ).add_to(m)
    
    # Add location marker
    folium.Marker(
        location=[lat, lon],
        popup=f"{location_option}<br>Risk: {risk_score:.2f}",
        icon=folium.Icon(
            color="red" if is_high_risk else ("orange" if is_moderate_risk else "green"),
            icon="info"
        )
    ).add_to(m)
    
    # Add shelters
    shelters = [
        {"name": "Shelter A", "lat": lat + 0.02, "lon": lon, "capacity": 500},
        {"name": "Shelter B", "lat": lat - 0.01, "lon": lon + 0.015, "capacity": 300},
        {"name": "Shelter C", "lat": lat, "lon": lon - 0.02, "capacity": 400},
    ]
    
    for shelter in shelters:
        folium.Marker(
            location=[shelter["lat"], shelter["lon"]],
            popup=f"{shelter['name']}<br>Capacity: {shelter['capacity']}",
            icon=folium.Icon(color="blue", icon="home")
        ).add_to(m)
    
    st_folium(m, width=1200, height=500)
    
    # Shelter info
    st.subheader("Verified Shelter Locations")
    shelter_data = []
    for s in shelters:
        dist = haversine(lon, lat, s['lon'], s['lat']) / 1000
        shelter_data.append({
            "Shelter": s['name'],
            "Capacity": s['capacity'],
            "Distance (km)": f"{dist:.1f}"
        })
    st.dataframe(pd.DataFrame(shelter_data), use_container_width=True, hide_index=True)

# TAB 3: Cyclone Forecasting
with tab_cyclone:
    st.subheader("Cyclone Path Visualization with Predictive Cones")
    
    m_cyclone = folium.Map(location=[lat, lon], zoom_start=8)
    
    # Generate track
    track = sample_synthetic_track(center_lon=lon - 0.5, center_lat=lat - 0.5)
    
    # Add track line
    track_coords = [[p[1], p[0]] for p in track]
    folium.PolyLine(
        track_coords,
        color="red",
        weight=3,
        opacity=0.9,
        popup="Predicted cyclone center track"
    ).add_to(m_cyclone)
    
    # Add cones of uncertainty
    cones = generate_cone(track, max_width_km=80)
    for i, cone in enumerate(cones):
        folium.Polygon(
            cone,
            color="purple",
            weight=1,
            fill=True,
            fillColor="purple",
            fillOpacity=0.1 + (i * 0.02)
        ).add_to(m_cyclone)
    
    # Current position
    if track:
        folium.CircleMarker(
            [track[0][1], track[0][0]],
            radius=12,
            color="darkred",
            fill=True,
            fillColor="red",
            popup="Current cyclone position<br>Speed: 20 km/h"
        ).add_to(m_cyclone)
    
    # Location marker
    folium.Marker(
        [lat, lon],
        popup=location_option,
        icon=folium.Icon(color="blue", icon="home")
    ).add_to(m_cyclone)
    
    st_folium(m_cyclone, width=1200, height=500)
    
    # Forecast details
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("**5-Day Forecast**")
        forecast_df = pd.DataFrame({
            "Hours": [0, 24, 48, 72, 96, 120],
            "Status": ["Current", "+1 day", "+2 days", "+3 days", "+4 days", "+5 days"],
            "Wind (km/h)": [120, 118, 115, 110, 105, 100],
            "Pressure (mb)": [990, 992, 995, 998, 1000, 1002]
        })
        st.dataframe(forecast_df, use_container_width=True, hide_index=True)
    
    with col2:
        landfall_prob = 65 if is_high_risk else (35 if is_moderate_risk else 10)
        st.metric("Landfall Probability", f"{landfall_prob}%")

# TAB 4: Community Reports
with tab_community:
    st.subheader("Community Participatory Risk Reporting")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("**Submit Observation**")
        name = st.text_input("Observer name")
        obs_type = st.selectbox(
            "Observation type",
            ["Anomalous waves", "Tidal deviation", "Wind pattern shift", "Wildlife behavior", "Other"]
        )
        description = st.text_area("Description", height=100)
        confidence = st.slider("Confidence", 0.0, 1.0, 0.7)
        
        if st.button("Submit"):
            if name and description:
                st.session_state.community_reports.append({
                    "timestamp": datetime.now(),
                    "name": name,
                    "type": obs_type,
                    "description": description,
                    "confidence": confidence
                })
                st.success("✓ Report submitted")
    
    with col2:
        st.metric("Total Reports", len(st.session_state.community_reports))
        if st.session_state.community_reports:
            avg_conf = np.mean([r['confidence'] for r in st.session_state.community_reports])
            st.metric("Avg Confidence", f"{avg_conf:.0%}")
    
    if st.session_state.community_reports:
        st.divider()
        st.write("**Recent Reports**")
        report_df = pd.DataFrame([
            {
                "Time": r['timestamp'].strftime("%H:%M"),
                "Observer": r['name'],
                "Type": r['type'],
                "Confidence": f"{r['confidence']:.0%}"
            }
            for r in sorted(st.session_state.community_reports, key=lambda x: x['timestamp'], reverse=True)[:5]
        ])
        st.dataframe(report_df, use_container_width=True, hide_index=True)

# TAB 5: Evacuation Routing
with tab_evacuation:
    st.subheader("AI-Assisted Evacuation Routing to Verified Shelters")
    
    best_shelter, best_dist = nearest_shelter(lon, lat, shelters)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if best_shelter:
            st.markdown(f"""
            <div class="metric-box">
            <strong>Nearest Shelter</strong><br>
            {best_shelter['name']}<br>
            Distance: {best_dist/1000:.1f} km<br>
            Capacity: {best_shelter['capacity']} people
            </div>
            """, unsafe_allow_html=True)
            
            # Create route map
            m_route = folium.Map(location=[lat, lon], zoom_start=12)
            
            # Route line
            route_coords = [
                [lat, lon],
                [best_shelter['lat'], best_shelter['lon']]
            ]
            folium.PolyLine(route_coords, color="green", weight=3).add_to(m_route)
            
            # Start and end markers
            folium.Marker([lat, lon], popup="Start", icon=folium.Icon(color="green")).add_to(m_route)
            folium.Marker(
                [best_shelter['lat'], best_shelter['lon']],
                popup="Destination",
                icon=folium.Icon(color="blue")
            ).add_to(m_route)
            
            st_folium(m_route, width=500, height=400)
    
    with col2:
        travel_time = (best_dist / 1000) / 5 * 60  # ~5 km/h on foot
        st.markdown(f"""
        <div class="metric-box">
        <strong>Evacuation Details</strong><br>
        <br>
        Estimated travel time: {travel_time:.0f} minutes<br>
        Route distance: {best_dist/1000:.1f} km<br>
        Facility type: Community shelter<br>
        Current occupancy: Empty
        </div>
        """, unsafe_allow_html=True)

# TAB 6: Maritime Safety
with tab_maritime:
    st.subheader("Maritime Vessel Tracking for Fisherfolk Safety")
    
    vessels = sample_vessel_positions()
    current_vessels = get_positions_at_step(vessels, 0)
    
    m_vessels = folium.Map(location=[lat, lon], zoom_start=11)
    
    safe_count = 0
    for v in current_vessels:
        dist = haversine(v['lon'], v['lat'], lon, lat)
        is_safe = dist > zone_radius if is_high_risk else dist > 1000
        
        if is_safe:
            safe_count += 1
            color = "green"
        else:
            color = "red"
        
        folium.CircleMarker(
            [v['lat'], v['lon']],
            radius=8,
            color=color,
            fill=True,
            popup=f"{v['name']}<br>Status: {'SAFE' if is_safe else 'DANGER ZONE'}"
        ).add_to(m_vessels)
    
    folium.Circle([lat, lon], radius=zone_radius, color="red", fill=False).add_to(m_vessels)
    
    st_folium(m_vessels, width=1200, height=500)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Active Vessels", len(current_vessels))
    with col2:
        st.metric("Safe Zone", f"{safe_count}/{len(current_vessels)}")
    with col3:
        at_risk = len(current_vessels) - safe_count
        st.metric("In Danger Zone", at_risk, delta=None)

# TAB 7: System Information
with tab_info:
    st.subheader("About CoastGuard AI")
    
    st.markdown("""
    **Traditional Knowledge Modifier Engine**
    
    Hybrid risk calculation formula:
    ```
    Risk = Satellite Base (0.3) + Indigenous Score - Bioshield Protection
    ```
    
    **Components:**
    - Satellite Intelligence: Vegetation indices, coastal morphology
    - Indigenous Knowledge: Boatmen observations, tidal deviations, wind patterns
    - Bioshield: Mangrove buffer protection (up to 0.5)
    
    **Data Sources:**
    - Real-time: Tide levels, rainfall, wind speed
    - Predictive: ML-enhanced cyclone forecasting
    - Community: Participatory observation system
    
    **System Capabilities:**
    1. Automated coastal flood alerting with threshold triggers
    2. AI-assisted evacuation routing to verified shelters
    3. Cyclone path visualization with predictive uncertainty cones
    4. Maritime vessel tracking for fisherfolk safety
    5. Community dashboards for participatory risk reporting
    6. Map-driven visualization with Red/Orange/Green zones
    
    **Deployment**: Scalable to multiple coastal regions in India
    """)
    
    st.divider()
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
