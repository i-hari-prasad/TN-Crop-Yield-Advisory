"""
Prediction Page — XGBoost yield prediction with SHAP explainability.
"""
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from utils.district_coords import DISTRICTS, CROPS, SEASONS
from utils.weather_api import get_live_weather

st.set_page_config(page_title="Prediction | TN Crop Advisory", page_icon="🔮", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;}
.stApp{background:#f0ede6;}
[data-testid="stSidebar"]{background:#1c3a1c !important;}
[data-testid="stSidebarNav"] a{color:rgba(255,255,255,0.75)!important;border-radius:8px;padding:8px 12px;transition:all 0.2s;}
[data-testid="stSidebarNav"] a:hover,[data-testid="stSidebarNav"] a[aria-current="page"]{background:rgba(255,255,255,0.12)!important;color:white!important;}
[data-testid="stSidebarNav"] span{color:inherit!important;}
.stButton>button{background:#2d6a2a;color:white;border:none;border-radius:10px;padding:11px 26px;font-weight:600;transition:all 0.25s;box-shadow:0 4px 14px rgba(45,106,42,0.25);}
.stButton>button:hover{background:#245522;box-shadow:0 6px 20px rgba(45,106,42,0.4);transform:translateY(-1px);}
[data-testid="metric-container"]{background:white;border-radius:14px;padding:20px 18px;box-shadow:0 2px 10px rgba(0,0,0,0.06);border-bottom:3px solid #2d6a2a;}
[data-testid="stMetricValue"]{color:#1c3a1c!important;font-size:2rem!important;font-weight:700!important;}
.stTabs [data-baseweb="tab-list"]{gap:4px;background:#e8e3d8;padding:4px;border-radius:12px;}
.stTabs [data-baseweb="tab"]{border-radius:9px;padding:8px 20px;font-weight:500;color:#555;}
.stTabs [aria-selected="true"]{background:white!important;color:#1c3a1c!important;box-shadow:0 2px 6px rgba(0,0,0,0.1);}
#MainMenu,footer,header{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style="padding:20px 16px 12px;">
        <div style="font-size:2rem;margin-bottom:8px;">🌾</div>
        <div style="color:white;font-size:1.1rem;font-weight:700;font-family:'DM Serif Display',serif;">TN Crop Advisory</div>
        <div style="color:rgba(255,255,255,0.5);font-size:0.78rem;margin-top:4px;">AI · XGBoost · SHAP</div>
    </div>
    <div style="height:1px;background:rgba(255,255,255,0.1);margin:0 16px 12px;"></div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="margin-bottom:24px;">
  <h1 style="color:#1c3a1c;font-family:'DM Serif Display',serif;font-size:2rem;border-bottom:3px solid #2d6a2a;padding-bottom:10px;margin-bottom:6px;">
    🔮 Yield Prediction
  </h1>
  <p style="color:#666;margin:0;">Select your farm details below and get an AI-powered yield forecast with factor breakdown.</p>
</div>
""", unsafe_allow_html=True)

# ── Load models ───────────────────────────────────────────────────────────────
@st.cache_resource
def load_assets():
    models_dir = Path(__file__).parent.parent.parent / "models"
    data_dir   = Path(__file__).parent.parent.parent / "data" / "processed"
    try:
        xgb   = joblib.load(models_dir / 'xgboost_model.pkl')
        le_d  = joblib.load(models_dir / 'le_district.pkl')
        le_c  = joblib.load(models_dir / 'le_crop.pkl')
        le_s  = joblib.load(models_dir / 'le_season.pkl')
        scaler= joblib.load(models_dir / 'scaler.pkl')
        feats = joblib.load(models_dir / 'feature_names.pkl')
        df    = pd.read_csv(data_dir / 'engineered_data.csv')
        return xgb, le_d, le_c, le_s, scaler, feats, df
    except Exception as e:
        st.error(f"Could not load models. Have you run setup.py? → {e}")
        return [None]*7

xgb_model, le_dist, le_crop, le_seas, scaler, feature_names, df_hist = load_assets()
if xgb_model is None:
    st.stop()

# ── SHAP (lazy import to avoid crash if not installed) ────────────────────────
@st.cache_resource
def get_explainer():
    try:
        import shap
        return shap.TreeExplainer(xgb_model)
    except Exception:
        return None

# ── Step 1 — Farm Details ─────────────────────────────────────────────────────
st.markdown('<div style="background:white;border-radius:14px;padding:24px;box-shadow:0 2px 10px rgba(0,0,0,0.06);margin-bottom:20px;">', unsafe_allow_html=True)
st.markdown("### 1 · Select Farm Details")
col1, col2, col3 = st.columns(3)
with col1: district = st.selectbox("District", sorted(DISTRICTS.keys()))
with col2: crop     = st.selectbox("Crop",     CROPS)
with col3: season   = st.selectbox("Season",   SEASONS)
st.markdown('</div>', unsafe_allow_html=True)

# Historical context
hist = df_hist[(df_hist['district'] == district) & (df_hist['crop'] == crop)]
avg_yield  = hist['yield_t_ha'].mean()  if len(hist) > 0 else 2.5
last_yield = hist.sort_values('year').iloc[-1]['yield_t_ha'] if len(hist) > 0 else 2.5
avg_rain   = hist['rainfall_mm'].mean() if len(hist) > 0 else 1000

# ── Step 2 — Weather ─────────────────────────────────────────────────────────
st.markdown('<div style="background:white;border-radius:14px;padding:24px;box-shadow:0 2px 10px rgba(0,0,0,0.06);margin-bottom:20px;">', unsafe_allow_html=True)
st.markdown("### 2 · Environmental Factors")
use_live = st.toggle("Fetch Live Weather (OpenWeatherMap)", value=False)
if use_live:
    with st.spinner("Fetching weather..."):
        w = get_live_weather(DISTRICTS[district]["lat"], DISTRICTS[district]["lon"])
        default_temp = w["temp_c"]
else:
    default_temp = 30.0

cw1, cw2, cw3 = st.columns(3)
with cw1: rainfall = st.slider("Annual Rainfall (mm)", 300, 3000, int(avg_rain))
with cw2: temp     = st.slider("Avg Temperature (°C)", 20.0, 40.0, float(round(default_temp,1)), 0.1)
with cw3: fert     = st.slider("Fertilizer (kg/ha)",  50,  400,  150)
st.markdown('</div>', unsafe_allow_html=True)

# ── Step 3 — Soil ─────────────────────────────────────────────────────────────
st.markdown('<div style="background:white;border-radius:14px;padding:24px;box-shadow:0 2px 10px rgba(0,0,0,0.06);margin-bottom:20px;">', unsafe_allow_html=True)
st.markdown("### 3 · Soil Health (NPK & pH)")
with st.expander("Adjust Soil Parameters", expanded=False):
    cs1,cs2,cs3,cs4 = st.columns(4)
    with cs1: soil_N  = st.slider("Nitrogen (N)",    100, 400, 250)
    with cs2: soil_P  = st.slider("Phosphorus (P)",  10,  60,  25)
    with cs3: soil_K  = st.slider("Potassium (K)",   100, 350, 200)
    with cs4: soil_pH = st.slider("Soil pH",         4.0, 9.0, 6.8, 0.1)
st.markdown('</div>', unsafe_allow_html=True)

# Derived features
fert_score = (soil_N/300*0.4 + soil_P/35*0.3 + soil_K/280*0.3) * max(0.1, 1 - 0.3*abs(soil_pH - 6.8))

# ── Predict ───────────────────────────────────────────────────────────────────
if st.button("🔮 Predict Yield", type="primary", use_container_width=True):
    try:
        dist_enc = le_dist.transform([district])[0]
    except Exception:
        dist_enc = 0
    try:
        crop_enc = le_crop.transform([crop])[0]
    except Exception:
        crop_enc = 0
    try:
        seas_enc = le_seas.transform([season])[0]
    except Exception:
        seas_enc = 0

    input_df = pd.DataFrame([{
        'rainfall_mm':       rainfall,
        'rainfall_3yr_avg':  avg_rain,
        'temp_avg_c':        temp,
        'soil_N':            soil_N,
        'soil_P':            soil_P,
        'soil_K':            soil_K,
        'soil_pH':           soil_pH,
        'soil_fertility_score': fert_score,
        'ndvi':              0.55,
        'fertilizer_kg_ha':  fert,
        'yield_lag1':        last_yield,
        'district_encoded':  dist_enc,
        'crop_encoded':      crop_enc,
        'season_encoded':    seas_enc,
    }])[feature_names]

    input_scaled = scaler.transform(input_df)

    with st.spinner("Running XGBoost model..."):
        pred = float(xgb_model.predict(input_scaled)[0])

    diff = pred - avg_yield

    # Save for advisory
    st.session_state['last_prediction'] = {
        'district': district, 'crop': crop, 'season': season,
        'yield_pred': pred, 'district_avg': avg_yield,
        'weather_temp': temp, 'weather_rain': rainfall,
        'input_data': input_df, 'top_factors': []
    }

    st.markdown("<hr style='margin:24px 0;border:none;border-top:1px solid #e0dbd0;'>", unsafe_allow_html=True)

    res_col, shap_col = st.columns([1, 2], gap="large")

    with res_col:
        st.markdown("### Result")

        # Gauge
        max_g = max(avg_yield * 2.5, pred * 1.3, 5.0)
        color_g = "#2d6a2a" if diff >= 0 else "#d9534f"
        gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=pred,
            delta={"reference": avg_yield, "valueformat": ".2f", "suffix": " t/ha vs avg"},
            number={"suffix": " t/ha", "valueformat": ".2f",
                    "font": {"size": 34, "color": color_g, "family": "DM Sans"}},
            title={"text": f"{crop} · {district}", "font": {"size": 13, "color": "#555", "family": "DM Sans"}},
            gauge={
                "axis": {"range": [0, max_g]},
                "bar":  {"color": color_g},
                "bgcolor": "white",
                "borderwidth": 1, "bordercolor": "#e0dbd0",
                "steps": [
                    {"range": [0,            avg_yield*0.85], "color": "rgba(217,83,79,0.08)"},
                    {"range": [avg_yield*0.85,avg_yield*1.05],"color": "rgba(240,173,78,0.08)"},
                    {"range": [avg_yield*1.05,max_g],         "color": "rgba(45,106,42,0.08)"},
                ],
                "threshold": {"line": {"color": "#1c3a1c","width": 2},
                              "thickness": 0.75, "value": avg_yield}
            }
        ))
        gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=260,
                            margin=dict(l=20,r=20,t=30,b=0),
                            font=dict(family="DM Sans"))
        st.plotly_chart(gauge, use_container_width=True)

        # Badge
        if diff > 0.5:
            badge = ("🌟 Excellent", "#2d6a2a")
        elif diff >= 0:
            badge = ("✅ Good", "#4caf50")
        elif diff >= -0.3:
            badge = ("⚠️ Average", "#f0ad4e")
        else:
            badge = ("🔴 Below Average", "#d9534f")

        st.markdown(f"""
        <div style="text-align:center;margin-bottom:16px;">
          <span style="background:{badge[1]};color:white;padding:5px 16px;
                border-radius:20px;font-weight:600;font-size:0.9rem;">{badge[0]}</span>
        </div>
        """, unsafe_allow_html=True)

        st.metric("Predicted Yield", f"{pred:.2f} t/ha",
                  f"{diff:+.2f} vs district avg ({avg_yield:.2f})",
                  delta_color="normal" if diff >= 0 else "inverse")

        st.info("💡 Go to **Advisory** page for your PDF action plan!")

    with shap_col:
        st.markdown("### Why This Prediction? (SHAP)")
        st.caption("Green = positive contribution  ·  Red = negative contribution")

        explainer = get_explainer()
        if explainer is not None:
            try:
                import shap, matplotlib
                matplotlib.use("Agg")
                import matplotlib.pyplot as plt

                shap_vals = explainer(input_scaled)
                vals = shap_vals.values[0]
                abs_vals = np.abs(vals)
                total = np.sum(abs_vals)
                pcts  = (abs_vals / total * 100) if total > 0 else np.zeros_like(abs_vals)

                name_map = {
                    'rainfall_mm':'Rainfall','rainfall_3yr_avg':'Hist. Rainfall',
                    'temp_avg_c':'Temperature','soil_N':'Soil Nitrogen',
                    'soil_P':'Soil Phosphorus','soil_K':'Soil Potassium',
                    'soil_pH':'Soil pH','soil_fertility_score':'Soil Fertility',
                    'ndvi':'NDVI (Vegetation)','fertilizer_kg_ha':'Fertilizer',
                    'yield_lag1':'Previous Yield','district_encoded':'District',
                    'crop_encoded':'Crop Type','season_encoded':'Season'
                }
                df_shap = pd.DataFrame({'Feature': [name_map.get(f,f) for f in feature_names],
                                        'Impact': vals, 'Pct': pcts})
                df_shap = df_shap[df_shap['Pct'] > 1.0].sort_values('Pct')

                fig_s, ax = plt.subplots(figsize=(8, 5))
                fig_s.patch.set_facecolor('#f9f7f2')
                ax.set_facecolor('#f9f7f2')
                colors = ['#2d6a2a' if v > 0 else '#d9534f' for v in df_shap['Impact']]
                bars = ax.barh(df_shap['Feature'], df_shap['Pct'], color=colors,
                               edgecolor='none', height=0.6)
                for bar in bars:
                    w = bar.get_width()
                    ax.text(w+0.3, bar.get_y()+bar.get_height()/2, f'{w:.1f}%',
                            va='center', fontsize=9, color='#333', fontweight='600')
                ax.set_xlabel('Relative Contribution (%)', fontsize=10, color='#555')
                ax.set_title('Factors Affecting Predicted Yield', fontsize=13,
                             fontweight='bold', color='#1c3a1c', pad=12)
                ax.spines[['top','right','bottom']].set_visible(False)
                ax.spines['left'].set_color('#ddd')
                ax.tick_params(colors='#555', labelsize=9)
                ax.xaxis.set_tick_params(color='#ddd')
                plt.tight_layout()
                st.pyplot(fig_s)

                # Save top factors
                top_factors = []
                for _, row in df_shap.sort_values('Pct', ascending=False).head(3).iterrows():
                    top_factors.append({'name': row['Feature'], 'percentage': row['Pct'], 'impact': row['Impact']})
                st.session_state['last_prediction']['top_factors'] = top_factors

            except Exception as e:
                st.warning(f"SHAP chart unavailable: {e}")
        else:
            st.warning("SHAP unavailable — prediction above is still valid.")

    # Historical trend
    if len(hist) > 0:
        st.markdown("### Historical Trend — Last 5 Years")
        recent = hist.sort_values('year').tail(5)
        fig_t = go.Figure()
        fig_t.add_trace(go.Scatter(x=recent['year'], y=recent['yield_t_ha'],
                                   mode='lines+markers+text',
                                   line=dict(color='#2d6a2a', width=2.5),
                                   marker=dict(size=8, color='#2d6a2a'),
                                   text=recent['yield_t_ha'].apply(lambda v: f'{v:.2f}'),
                                   textposition='top center',
                                   fill='tozeroy', fillcolor='rgba(45,106,42,0.07)'))
        fig_t.add_hline(y=pred, line_dash='dash', line_color='#d9534f', line_width=1.5,
                        annotation_text=f'Predicted: {pred:.2f}', annotation_position='right')
        fig_t.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                            height=280, margin=dict(l=0,r=60,t=10,b=0),
                            font=dict(family='DM Sans',color='#333'),
                            xaxis=dict(title='Year', showgrid=True, gridcolor='#e8e3d8'),
                            yaxis=dict(title='Yield (t/ha)', showgrid=True, gridcolor='#e8e3d8'))
        st.plotly_chart(fig_t, use_container_width=True)
