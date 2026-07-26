# 🌊 CoastGuard AI — Maritime Early Warning Climate System

[![Python](https://img.shields.io/badge/Python-v3.10+-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-v1.28+-red.svg?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-v2.x-orange.svg?style=for-the-badge&logo=tensorflow)](https://www.tensorflow.org/)
[![Live Demo](https://img.shields.io/badge/Live_Demo-Streamlit-red.svg?style=for-the-badge&logo=streamlit)](https://coastguard-by-krishna-kanhaiya.streamlit.app/)

> **CoastGuard AI is a hybrid early warning climate intelligence platform that merges satellite geospatial data with crowdsourced indigenous community reports.** Delivers hyperlocal hazard scores, cyclone tracking, bioshield analysis, and automated emergency evacuation routes.

---

## 🌐 Live Application
👉 **[Launch CoastGuard AI Web App](https://coastguard-by-krishna-kanhaiya.streamlit.app/)**

---

## 💡 Data Fusion Architecture

```mermaid
graph LR
    Sat[Satellite Geospatial Intelligence] --> Fusion[Hybrid Data Fusion Engine]
    Community[Indigenous Community Crowdsourced Reports] --> Fusion
    Fusion --> ML[Predictive Cyclone & Coastal Flood Model]
    ML --> UI[Streamlit Interactive Dashboard]
    UI --> Alert[Hyperlocal Risk Scores & Evacuation Routes]
```

---

## ✨ UI Features & Functionality Inventory

| UI Feature Module | Interactive Functionality | Real User Flow |
| :--- | :--- | :--- |
| **Interactive Satellite Map** | Renders real-time sea surface temperature, mangrove density, and coastal erosion maps. | Toggle geospatial layers $\rightarrow$ Hover over coastal zones to inspect temperature & risk indexes. |
| **Indigenous Community Alert Form** | Allows local fishermen and residents to submit real-time wave/surge reports. | Fill surge observation form $\rightarrow$ Submit report $\rightarrow$ Pins community report on map. |
| **Cyclone Risk Calculator** | Computes hyperlocal hazard scores based on storm trajectory and coastal elevation. | Input wind speed & pressure $\rightarrow$ Click "Assess Hazard Score" $\rightarrow$ View risk meter gauge. |
| **Emergency Evacuation Router** | Calculates shortest safe evacuation paths from hazard zones to storm shelters. | Select starting district $\rightarrow$ Click "Generate Evacuation Route" $\rightarrow$ Displays step-by-step route map. |

---

## 🛠️ Local Developer Setup

```bash
git clone https://github.com/KrishnaKanhaiya1/CoastGuardAI.git
cd CoastGuardAI
pip install -r requirements.txt
streamlit run app_integrated.py
```
