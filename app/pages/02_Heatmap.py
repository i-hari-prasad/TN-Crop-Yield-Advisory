"""
District Heatmap Page — Folium interactive map with yield predictions for all 38 districts.
"""
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import joblib
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from utils.district_coords import DISTRICTS, CROPS

st.set_page_config(page_title="Heatmap | TN Crop Advisory", page_icon="🗺️", layout="wide")

SHARED_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;}
.stApp{background:#f0ede6;}
[data-testid="stSidebar"]{background:#1c3a1c !important;}
[data-testid="stSidebarNav"] a{color:rgba(255,255,255,0.75)!important;border-radius:8px;padding:8px 12px;transition:all 0.2s;}
[data-testid="stSidebarNav"] a:hover,[data-testid="stSidebarNav"] a[aria-current="page"]{background:rgba(255,255,255,0.12)!important;color:white!important;}
[data-testid="stSidebarNav"] span{color:inherit!important;}
.stButton>button{background:#2d6a2a;color:white;border:none;border-radius:10px;padding:11px 26px;font-weight:600;transition:all 0.25s;box-shadow:0 4px 14px rgba(45,106,42,0.25);}
.stButton>button:hover{background:#245522;transform:translateY(-1px);}
#MainMenu,footer,header{visibility:hidden;}
</style>
"""
st.markdown(SHARED_CSS, unsafe_allow_html=True)

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
    🗺️ District Yield Heatmap
  </h1>
  <p style="color:#666;margin:0;">Generate an interactive map of predicted yield potential across all 38 Tamil Nadu districts.</p>
</div>
""", unsafe_allow_html=True)

# ── Load assets ───────────────────────────────────────────────────────────────
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
        st.error(f"Could not load models: {e}")
        return [None]*7

xgb_model, le_dist, le_crop, le_seas, scaler, feature_names, df_hist = load_assets()
if xgb_model is None:
    st.stop()

# ── Controls ──────────────────────────────────────────────────────────────────
st.markdown('<div style="background:white;border-radius:14px;padding:24px;box-shadow:0 2px 10px rgba(0,0,0,0.06);margin-bottom:20px;">', unsafe_allow_html=True)
cc1, cc2 = st.columns(2)
with cc1:
    crop = st.selectbox("Select Crop", CROPS, index=0)
with cc2:
    avail = df_hist[df_hist['crop'] == crop]['season'].unique().tolist()
    if not avail:
        avail = ["Kharif"]
    season = st.selectbox("Select Season", avail)
st.markdown('</div>', unsafe_allow_html=True)

if st.button("🗺️ Generate Heatmap for All 38 Districts", type="primary", use_container_width=True):
    with st.spinner("Predicting yields for all 38 districts..."):
        rows = []
        for dist, info in DISTRICTS.items():
            h = df_hist[(df_hist['district'] == dist) & (df_hist['crop'] == crop)]
            if len(h) > 0:
                avg_rain  = h['rainfall_mm'].mean()
                avg_temp  = h['temp_avg_c'].mean()
                last_yield= h.sort_values('year').iloc[-1]['yield_t_ha']
                soil_N    = h['soil_N'].mean()
                soil_P    = h['soil_P'].mean()
                soil_K    = h['soil_K'].mean()
                soil_pH   = h['soil_pH'].mean()
                fert_score= h['soil_fertility_score'].mean()
                fert      = h['fertilizer_kg_ha'].mean()
                hist_avg  = h['yield_t_ha'].mean()
            else:
                avg_rain, avg_temp, last_yield = 1000, 30.0, 2.5
                soil_N, soil_P, soil_K, soil_pH = 250, 25, 200, 6.8
                fert_score, fert, hist_avg = 0.5, 150, 2.5

            try:
                dist_enc = le_dist.transform([dist])[0]
            except Exception:
                dist_enc = 0
            try:
                seas_enc = le_seas.transform([season])[0]
            except Exception:
                seas_enc = 0
            try:
                crop_enc = le_crop.transform([crop])[0]
            except Exception:
                crop_enc = 0

            inp = pd.DataFrame([{
                'rainfall_mm': avg_rain, 'rainfall_3yr_avg': avg_rain,
                'temp_avg_c': avg_temp, 'soil_N': soil_N, 'soil_P': soil_P,
                'soil_K': soil_K, 'soil_pH': soil_pH,
                'soil_fertility_score': fert_score, 'ndvi': 0.55,
                'fertilizer_kg_ha': fert, 'yield_lag1': last_yield,
                'district_encoded': dist_enc, 'crop_encoded': crop_enc,
                'season_encoded': seas_enc,
            }])[feature_names]
            pred = float(xgb_model.predict(scaler.transform(inp))[0])
            rows.append({'District': dist, 'Lat': info['lat'], 'Lon': info['lon'],
                         'Predicted': pred, 'HistAvg': hist_avg})

        df_pred = pd.DataFrame(rows)
        mn, mx = df_pred['Predicted'].min(), df_pred['Predicted'].max()

    st.markdown("---")
    legend_html = """
    <div style="display:flex;gap:20px;align-items:center;margin-bottom:12px;padding:12px 16px;
         background:white;border-radius:10px;box-shadow:0 2px 8px rgba(0,0,0,0.06);width:fit-content;">
      <b style="color:#333;">Yield vs Historical Avg:</b>
      <span>🟢 Above average</span>
      <span>🟡 Near average</span>
      <span>🔴 Below average</span>
    </div>
    """
    st.markdown(legend_html, unsafe_allow_html=True)

    # Build Folium map
    m = folium.Map(location=[11.1271, 78.6569], zoom_start=7,
                   tiles="CartoDB positron",
                   attr="CartoDB")

    for _, row in df_pred.iterrows():
        norm = (row['Predicted'] - mn) / (mx - mn + 0.001)
        if row['Predicted'] > row['HistAvg'] * 1.05:
            clr = '#2d6a2a'
        elif row['Predicted'] < row['HistAvg'] * 0.95:
            clr = '#d9534f'
        else:
            clr = '#f0ad4e'

        diff_pct = (row['Predicted'] - row['HistAvg']) / row['HistAvg'] * 100 if row['HistAvg'] > 0 else 0
        popup_html = f"""
        <div style="font-family:Arial;min-width:160px;padding:4px;">
          <b style="font-size:14px;color:#1c3a1c;">{row['District']}</b><hr style="margin:4px 0;">
          <b>Crop:</b> {crop}<br>
          <b>Season:</b> {season}<br>
          <b>Predicted:</b> <span style="color:{clr};font-weight:bold;">{row['Predicted']:.2f} t/ha</span><br>
          <b>Hist. Avg:</b> {row['HistAvg']:.2f} t/ha<br>
          <b>Δ vs avg:</b> {diff_pct:+.1f}%
        </div>
        """
        folium.CircleMarker(
            location=[row['Lat'], row['Lon']],
            radius=12 + norm * 10,
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"{row['District']}: {row['Predicted']:.2f} t/ha",
            color=clr, fill=True, fill_color=clr, fill_opacity=0.75,
            weight=2
        ).add_to(m)

    st_folium(m, width=None, height=560, returned_objects=[])

    # Table
    st.markdown("#### District Rankings")
    display = df_pred[['District','Predicted','HistAvg']].copy()
    display.columns = ['District', 'Predicted Yield (t/ha)', 'Historical Avg (t/ha)']
    display['vs Avg (%)'] = ((display['Predicted Yield (t/ha)'] - display['Historical Avg (t/ha)']) /
                              display['Historical Avg (t/ha)'] * 100).round(1)
    display = display.sort_values('Predicted Yield (t/ha)', ascending=False).reset_index(drop=True)
    display.index += 1
    st.dataframe(display.style.format({'Predicted Yield (t/ha)':'{:.2f}',
                                        'Historical Avg (t/ha)':'{:.2f}',
                                        'vs Avg (%)':'{:+.1f}%'}),
                 use_container_width=True)
