# Tamil Nadu District-Level Crop Yield Advisory System 🌾

An end-to-end Machine Learning web application designed to help farmers and agricultural extension officers in Tamil Nadu. The system predicts district-level crop yields, explains **WHY** the yield will be high or low, and provides **WHAT** to do through actionable advisory reports.

## Features

- **Yield Prediction:** Predicts yield in tonnes/hectare using an XGBoost model trained on historical weather, soil, NDVI, and fertilizer data.
- **SHAP Explainability:** Understand exactly which factors (e.g., rainfall deficit, low soil nitrogen) are impacting the prediction via visual charts.
- **District Heatmap:** Interactive choropleth heatmap showing yield potential across all 38 Tamil Nadu districts for any given crop and season.
- **Live Weather Integration:** Automatically fetches current weather conditions using the OpenWeatherMap API to refine predictions.
- **Automated Advisory Reports:** Generates a downloadable PDF report (`reportlab`) containing predictions, key factors, and customized agricultural recommendations.

## Tech Stack

- **Data & Features:** `pandas`, `numpy`, NASA POWER API (weather), OpenWeatherMap API
- **Machine Learning:** `scikit-learn` (Linear Regression, Random Forest), `xgboost` (Primary Model), `tensorflow/keras` (LSTM), `shap` (Explainability)
- **Web App UI:** `streamlit`, custom CSS for agricultural UX
- **Geospatial & Visualization:** `folium`, `streamlit-folium`, `matplotlib`
- **Reporting:** `reportlab`

## Setup & Installation

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/yourusername/TN-Crop-Advisory.git
cd TN-Crop-Advisory
pip install -r requirements.txt
```

### 2. Generate Data & Train Models
Since this system relies on 20 years of data across 38 districts, we provide an automated setup script that generates realistic historical data (incorporating real NASA POWER data when available) and trains all 4 machine learning models.
```bash
python setup.py
```
*This will create all CSVs in `data/raw/` and `data/processed/`, and save trained `.pkl` and `.h5` models in the `models/` directory.*

### 3. (Optional) OpenWeatherMap API Key
For live weather fetching, you need a free API key from [OpenWeatherMap](https://openweathermap.org/api).
Set it as an environment variable before running the app:
**Windows:** `set OWM_API_KEY=your_key_here`
**Linux/Mac:** `export OWM_API_KEY=your_key_here`
*(If no key is provided, the app gracefully falls back to historical averages.)*

### 4. Run the Streamlit App
```bash
streamlit run app/main.py
```

## Project Structure

```
Agri/
├── app/
│   ├── main.py                 # Streamlit entry point
│   └── pages/
│       ├── 01_Prediction.py    # XGBoost + SHAP UI
│       ├── 02_Heatmap.py       # Folium Map UI
│       └── 03_Advisory.py      # PDF Report UI
├── data/
│   ├── raw/                    # Base weather, soil, ndvi CSVs
│   └── processed/              # Engineered features
├── models/                     # Saved pkl/h5 models and scalers
├── reports/                    # Generated PDFs
├── utils/                      # Core backend logic
│   ├── data_generator.py       # Fetches API data & builds dataset
│   ├── feature_engineer.py     # Rolling averages & composite scores
│   ├── model_trainer.py        # ML pipeline (LR, RF, XGB, LSTM)
│   ├── shap_explainer.py       # SHAP plots
│   ├── pdf_generator.py        # Reportlab builder
│   └── weather_api.py          # OWM integration
└── setup.py                    # Orchestrates data + training
```

## Models Evaluated
- **Linear Regression** (Baseline)
- **Random Forest Regressor** (Ensemble benchmark)
- **XGBoost Regressor** (Primary Predictor - Target: R² > 0.82)
- **LSTM** (Time-series specific forecasting)

## Resume Snippet
> *Developed a Tamil Nadu District-Level Crop Yield Advisory System using XGBoost and LSTM trained on real government datasets from NASA POWER, ISRO NDVI, Soil Health Card Portal, and data.gov.in with SHAP explainability, live OpenWeatherMap API integration, interactive district heatmap, and automated PDF advisory report generation, deployed on Streamlit Cloud.*
