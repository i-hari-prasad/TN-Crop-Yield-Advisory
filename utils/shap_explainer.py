"""
SHAP explainability module. Explains XGBoost predictions.
"""
import shap
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
from pathlib import Path
import streamlit as st

MODELS_DIR = Path(__file__).parent.parent / "models"

@st.cache_resource
def load_explainer():
    """Load the XGBoost model and create a TreeExplainer."""
    model_path = MODELS_DIR / "xgboost_model.pkl"
    if not model_path.exists():
        return None, None
        
    xgb_model = joblib.load(model_path)
    explainer = shap.TreeExplainer(xgb_model)
    return xgb_model, explainer

def get_shap_values(input_features: pd.DataFrame):
    """Calculate SHAP values for the input."""
    xgb_model, explainer = load_explainer()
    if explainer is None:
        return None
        
    shap_vals = explainer.shap_values(input_features)
    return shap_vals[0] if isinstance(shap_vals, list) else shap_vals

def plot_shap_waterfall(input_features: pd.DataFrame, feature_names: list):
    """Generate a SHAP waterfall plot or bar chart for the prediction.
    Always returns a tuple (fig, df_impact) or (None, None).
    """
    try:
        xgb_model, explainer = load_explainer()
    except Exception:
        return None, None
    if explainer is None:
        return None, None
        
    try:
        shap_vals = explainer(input_features)
    except Exception:
        return None, None
    
    fig = plt.figure(figsize=(10, 6), facecolor="#F7F3E9")
    ax = fig.gca()
    ax.set_facecolor("#F7F3E9")
    
    # We use a bar chart to show percentage contribution as it's easier for users to understand
    # than a raw SHAP waterfall plot
    vals = shap_vals.values[0]
    
    # Normalize to percentages of total absolute impact
    abs_vals = np.abs(vals)
    total_impact = np.sum(abs_vals)
    if total_impact > 0:
        percentages = (abs_vals / total_impact) * 100
    else:
        percentages = np.zeros_like(abs_vals)
        
    # Create DataFrame for easier sorting
    df_impact = pd.DataFrame({
        'Feature': feature_names,
        'Impact_t_ha': vals,
        'Percentage': percentages
    })
    
    # Map raw feature names to human readable
    name_map = {
        'rainfall_mm': 'Rainfall',
        'rainfall_3yr_avg': 'Historical Rainfall',
        'temp_avg_c': 'Temperature',
        'soil_N': 'Soil Nitrogen (N)',
        'soil_P': 'Soil Phosphorus (P)',
        'soil_K': 'Soil Potassium (K)',
        'soil_pH': 'Soil pH',
        'soil_fertility_score': 'Overall Soil Fertility',
        'ndvi': 'Vegetation Index (NDVI)',
        'fertilizer_kg_ha': 'Fertilizer Applied',
        'yield_lag1': 'Previous Year Yield',
        'district_encoded': 'District Location',
        'crop_encoded': 'Crop Type',
        'season_encoded': 'Season'
    }
    
    df_impact['Feature'] = df_impact['Feature'].map(lambda x: name_map.get(x, x))
    
    # Filter out zero impact and sort
    df_impact = df_impact[df_impact['Percentage'] > 1.0].sort_values(by='Percentage', ascending=True)
    
    colors = ['#2D6A2A' if val > 0 else '#D9534F' for val in df_impact['Impact_t_ha']]
    
    bars = ax.barh(df_impact['Feature'], df_impact['Percentage'], color=colors, edgecolor='none')
    
    ax.set_xlabel('Relative Importance / Contribution (%)', fontsize=12, fontweight='bold', color="#1A1A2E")
    ax.set_title('Factors Impacting Predicted Yield', fontsize=16, fontweight='bold', color="#1A1A2E")
    ax.tick_params(axis='both', colors="#1A1A2E", labelsize=11)
    
    # Add text labels on bars
    for bar in bars:
        width = bar.get_width()
        label_x_pos = width + 0.5
        ax.text(label_x_pos, bar.get_y() + bar.get_height()/2, f'{width:.1f}%', 
                va='center', color="#1A1A2E", fontweight='bold')
                
    # Hide top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#1A1A2E')
    ax.spines['left'].set_color('#1A1A2E')
    
    plt.tight_layout()
    return fig, df_impact.sort_values(by='Percentage', ascending=False)

