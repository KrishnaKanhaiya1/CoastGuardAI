# 🌊 CoastGuard AI — Hybrid Maritime Climate Intelligence System

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg?style=for-the-badge&logo=tensorflow)](https://www.tensorflow.org/)
[![Live Demo](https://img.shields.io/badge/Live_Demo-Streamlit-red.svg?style=for-the-badge&logo=streamlit)](https://coastguard-by-krishna-kanhaiya.streamlit.app/)

> **A hybrid climate risk warning engine merging satellite geospatial intelligence with crowdsourced indigenous coastal knowledge.** Computes hyperlocal hazard scores, models storm surges, evaluates mangrove bioshield protection, and generates safe evacuation routes.

---

## 🌐 Live Application
👉 **[Launch CoastGuard AI Web Application](https://coastguard-by-krishna-kanhaiya.streamlit.app/)**

---

## 💡 Hybrid Data Fusion Pipeline

```mermaid
graph LR
    Sat[Satellite Geospatial Intelligence] --> Fusion[Hybrid Data Fusion Engine]
    Community[Indigenous Coastal Reports] --> Fusion
    Fusion --> ML[Predictive Cyclone & Flood Model]
    ML --> UI[Streamlit Interactive Dashboard]
    UI --> Alert[Hyperlocal Risk Scores & Evacuation Routes]
```

---

## 🧮 Hyperlocal Hazard Risk Equation

$$\text{Risk Score} = \min\left(100, \frac{\text{Wind Speed}}{200} \times 40 + \frac{1013 - \text{Pressure}}{80} \times 35 + \frac{\text{Surge Height}}{5} \times 25\right)$$

---

## 🛠️ Local Developer Setup

```bash
git clone https://github.com/KrishnaKanhaiya1/CoastGuardAI.git
cd CoastGuardAI
pip install -r requirements.txt
streamlit run app_integrated.py
```
