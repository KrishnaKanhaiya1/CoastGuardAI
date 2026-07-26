# 🌊 CoastGuard AI — Maritime Early Warning Climate System

[![Live Application](https://img.shields.io/badge/Live_Demo-Streamlit-FF4B4B.svg?style=for-the-badge&logo=streamlit)](https://coastguard-by-krishna-kanhaiya.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B.svg?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-FF6F00.svg?style=for-the-badge&logo=tensorflow)](https://www.tensorflow.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

A climate intelligence and early warning platform designed to safeguard coastal communities. **CoastGuard AI** merges quantitative satellite geospatial data with crowdsourced indigenous community knowledge to compute hyperlocal hazard scores, predict storm surges, and generate safe evacuation routes.

[🚀 Launch Live Application](https://coastguard-by-krishna-kanhaiya.streamlit.app/) • [📖 Data Fusion](#-hybrid-data-fusion) • [✨ Key Modules](#-key-modules) • [⚡ Getting Started](#-getting-started)

---

## 📌 Executive Summary

Coastal regions face risks from cyclones, sea-level rise, and sudden flooding. Existing regional weather alerts often lack hyperlocal precision and ignore ground-level observations from local fishing communities.

**CoastGuard AI** addresses this gap by fusing satellite data (Sea Surface Temperature, Vegetation Index, Barometric Pressure anomalies) with real-time community surge reports, delivering actionable risk scores and automated evacuation routing.

---

## 🏗️ Hybrid Data Fusion Architecture

```mermaid
flowchart LR
    SatData[Satellite Geospatial Data] --> FusionEngine[Data Fusion & Feature Engine]
    CommunityData[Crowdsourced Coastal Reports] --> FusionEngine
    
    FusionEngine --> HazardModel[Predictive Hazard Model]
    HazardModel --> RiskScore[Hyperlocal Risk Score Calculation]
    
    RiskScore --> UI[Streamlit Dashboard]
    UI --> MapView[Interactive Map & Evacuation Routes]
```

---

## ✨ Key Modules

### 🛰️ Geospatial Hazard Mapping
* **Satellite Data Layers**: Visualizes sea surface temperature variations, coastal vegetation density, and cyclone track forecasts.
* **Hyperlocal Risk Gauge**: Computes dynamic hazard indexes (Low, Moderate, High, Extreme Danger) based on barometric pressure and wind speeds.

### 👥 Community Alert Network
* **Crowdsourced Report Submission**: Enables local residents and coastal authorities to submit ground observations (wave height, sea behavior).
* **Map Verification**: Displays crowdsourced alerts alongside satellite layers for multi-source verification.

### 🚗 Emergency Evacuation Router
* **Evacuation Guidance**: Calculates safe paths from high-risk coastal sectors to designated storm shelters.

---

## 💻 Tech Stack

* **Language**: Python 3.10+
* **Framework**: Streamlit
* **Machine Learning**: TensorFlow, Scikit-Learn
* **Geospatial Processing**: Folium, GeoPandas, OpenStreetMap APIs

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

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
