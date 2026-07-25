# CoastGuard AI — Maritime Early Warning System

[![CI Build](https://github.com/KrishnaKanhaiya1/CoastGuardAI/actions/workflows/ci.yml/badge.svg)](https://github.com/KrishnaKanhaiya1/CoastGuardAI/actions/workflows/ci.yml)
[![Live Demo](https://img.shields.io/badge/Live_Demo-Streamlit_Cloud-red.svg?style=for-the-badge&logo=streamlit)](https://coastguard-by-krishna-kanhaiya.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)](https://www.tensorflow.org/)

CoastGuard AI is a hybrid early warning climate platform that merges satellite geospatial data (vegetation index, sea surface temperature, cyclone track models) with crowdsourced indigenous community reports to output hyperlocal hazard scores and evacuation routes.

---

## 🌐 Live Application
👉 **[Open Live Streamlit Application](https://coastguard-by-krishna-kanhaiya.streamlit.app/)**

---

## ⚙️ Data Fusion Architecture

```mermaid
graph LR
    Sat[Satellite Geospatial Intelligence] --> Fusion[Hybrid Fusion Engine]
    Community[Crowdsourced Coastal Reports] --> Fusion
    Fusion --> ML[Predictive Cyclone & Flood Model]
    ML --> Alert[Hyperlocal Risk Scores & Evacuation Routes]
```

---

## 🛠️ Local Execution

```bash
git clone https://github.com/KrishnaKanhaiya1/CoastGuardAI.git
cd CoastGuardAI
pip install -r requirements.txt
streamlit run app_integrated.py
```
