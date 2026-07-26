# CoastGuard AI — Maritime Early Warning Climate System

[![Live Application](https://img.shields.io/badge/Live_Demo-Streamlit-FF4B4B.svg?style=for-the-badge&logo=streamlit)](https://coastguard-by-krishna-kanhaiya.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B.svg?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-FF6F00.svg?style=for-the-badge&logo=tensorflow)](https://www.tensorflow.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

A hybrid climate intelligence and early warning platform designed to safeguard coastal communities. **CoastGuard AI** merges quantitative satellite geospatial data with qualitative crowdsourced indigenous community knowledge to compute hyperlocal hazard scores, predict storm surges, and generate safe evacuation routes.

[🚀 Explore Live Application](https://coastguard-by-krishna-kanhaiya.streamlit.app/) • [📖 View Architecture](#-hybrid-data-fusion) • [⚡ Local Setup](#-getting-started)

---

## 📌 Executive Overview

Coastal regions face increasing risks from cyclones, sea-level rise, and sudden flooding. Existing regional weather alerts often lack hyperlocal precision and ignore ground-level observations from local fishing communities.

**CoastGuard AI** addresses this gap by fusing satellite data (Sea Surface Temperature, Vegetation Index, Pressure anomalies) with real-time community surge reports, delivering actionable risk scores and automated evacuation routing.

---

## 🏗️ Hybrid Data Fusion

```mermaid
flowchart LR
    SatData[Satellite Geospatial Intelligence] --> FusionEngine[Data Fusion & Feature Engine]
    CommunityData[Crowdsourced Coastal Reports] --> FusionEngine
    
    FusionEngine --> HazardModel[Predictive Hazard Model]
    HazardModel --> RiskScore[Hyperlocal Risk Score Calculation]
    
    RiskScore --> UI[Streamlit Dashboard]
    UI --> MapView[Interactive Map & Evacuation Routes]
```

---

## ✨ Key Feature Modules

### 🛰️ Geospatial Risk Mapping
* **Satellite Data Layers**: Visualizes sea surface temperature variations, coastal vegetation density, and cyclone track forecasts.
* **Hyperlocal Risk Gauge**: Computes dynamic hazard indexes (Low, Moderate, High, Extreme Danger) based on barometric pressure and wind speeds.

### 👥 Community Alert Network
* **Crowdsourced Report Submission**: Enables local residents and coastal authorities to submit ground observations (wave height, unusual sea behavior).
* **Map Verification**: Displays crowdsourced alerts alongside satellite layers for multi-source verification.

### 🚗 Emergency Evacuation Router
* **Route Generation**: Calculates safe evacuation paths from high-risk coastal sectors to designated storm shelters.

---

## 🚀 Getting Started

### Prerequisites
* **Python**: `v3.10` or higher

### Installation & Run Commands
```bash
# Clone repository
git clone https://github.com/KrishnaKanhaiya1/CoastGuardAI.git
cd CoastGuardAI

# Install requirements
pip install -r requirements.txt

# Run Streamlit application
streamlit run app_integrated.py
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
