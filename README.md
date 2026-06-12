# TN Crop Yield Advisory System 🌾 | AI-Powered Agriculture Platform

An end-to-end Machine Learning full-stack application designed to help farmers, researchers, and agricultural extension officers in Tamil Nadu. The system predicts district-level crop yields, explains **WHY** the yield will be high or low using Explainable AI, and provides customized, downloadable advisory reports.

![Platform Overview](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![XGBoost](https://img.shields.io/badge/Machine%20Learning-XGBoost-blue?style=for-the-badge)
![Deep Learning](https://img.shields.io/badge/Deep%20Learning-LSTM-orange?style=for-the-badge)

## 🚀 Key Features

- **Yield Prediction:** Predicts yield in tonnes/hectare using an ensembled model (XGBoost, Random Forest, LSTM) trained on 20 years of historical weather, soil, and agricultural data.
- **SHAP Explainability (XAI):** See exactly which factors (e.g., rainfall deficit, low soil nitrogen) are impacting the prediction via interactive waterfall charts.
- **Geospatial Heatmap:** Interactive Folium choropleth map visualizing yield potential across all 38 Tamil Nadu districts.
- **Historical Trends:** Explore two decades of yield, rainfall, and temperature data through rich Plotly charts.
- **District Comparison:** Compare any two districts side-by-side using radar and bump charts to identify the best performing regions.
- **Automated PDF Advisory:** Instantly generate a downloadable, personalized agricultural action plan using `reportlab`.
- **Bilingual Interface:** A professional, responsive landing page with a native **English ↔ Tamil** toggle for local accessibility.

## 🛠️ Tech Stack

- **Data Engineering:** `pandas`, `numpy` (NASA POWER climate data, IMD rainfall, Soil Health Cards)
- **Machine Learning:** `scikit-learn`, `xgboost`, `tensorflow` (LSTM), `shap`
- **Web UI & Visualization:** `streamlit`, HTML/CSS (Landing Page), `plotly`, `folium`
- **Reporting:** `reportlab`

## ⚙️ Setup & Installation

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/i-hari-prasad/TN-Crop-Yield-Advisory.git
cd TN-Crop-Yield-Advisory
pip install -r requirements.txt
```

### 2. Run the Platform
You can run the Streamlit dashboard locally:
```bash
streamlit run app/main.py
```

*To view the custom HTML landing page with the English/Tamil toggle, open `index.html` in your browser.*

## 📂 Project Structure

```
TN-Crop-Yield-Advisory/
├── index.html                  # Professional bilingual landing page
├── app/
│   ├── main.py                 # Streamlit entry point & navigation
│   └── pages/
│       ├── 01_Prediction.py    # XGBoost + SHAP UI
│       ├── 02_Heatmap.py       # Folium Map UI
│       ├── 03_Advisory.py      # PDF Report UI
│       ├── 04_Trends.py        # Historical Data Analysis
│       └── 05_Compare.py       # District comparisons
├── data/
│   ├── raw/                    # Base weather, soil, ndvi datasets
│   └── processed/              # Engineered features
├── models/                     # Saved pkl/h5 models
├── reports/                    # Generated advisory PDFs
├── utils/                      # Core backend logic (Trainers, Explainers, APIs)
└── requirements.txt            # Python dependencies
```

## 🧠 Models Evaluated
- **XGBoost Regressor** (Primary Predictor - Best performance for non-linear interactions)
- **Random Forest Regressor** (Ensemble benchmark for variance handling)
- **LSTM Network** (Deep Learning for capturing multi-year time-series trends)
- **Linear Regression** (Baseline benchmark)

## 💼 Resume Snippet
> *Developed an end-to-end Crop Yield Advisory Platform for Tamil Nadu utilizing XGBoost, Random Forest, and LSTM models trained on 20 years of climate/soil data. Engineered 200+ features and integrated SHAP for model explainability. Built a full-stack Streamlit dashboard with geospatial heatmaps, interactive Plotly trend analysis, automated PDF report generation, and a bilingual HTML landing page.*
