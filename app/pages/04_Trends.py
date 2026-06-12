"""
Historical Trend Analysis Page.
Visualises yield, weather and soil trends over 20 years using Plotly.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from utils.district_coords import DISTRICTS, CROPS, SEASONS

st.set_page_config(
    page_title="Historical Trends | TN Crop Advisory",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;}
.stApp{background:#f0ede6;}
[data-testid="stSidebar"]{background:#1c3a1c !important;}
[data-testid="stSidebarNav"] a{color:rgba(255,255,255,0.75)!important;border-radius:8px;padding:8px 12px;transition:all 0.2s;}
[data-testid="stSidebarNav"] a:hover,[data-testid="stSidebarNav"] a[aria-current="page"]{background:rgba(255,255,255,0.12)!important;color:white!important;}
[data-testid="stSidebarNav"] span{color:inherit!important;}
[data-testid="metric-container"]{background:white;border-radius:14px;padding:20px 18px;box-shadow:0 2px 10px rgba(0,0,0,0.06);border-bottom:3px solid #2d6a2a;}
[data-testid="stMetricValue"]{color:#1c3a1c!important;font-size:2rem!important;font-weight:700!important;}
#MainMenu,footer,header{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="margin-bottom:24px;">
  <h1 style="color:#1c3a1c;font-family:'DM Serif Display',serif;font-size:2rem;border-bottom:3px solid #2d6a2a;padding-bottom:10px;margin-bottom:6px;">
    📈 Historical Trends
  </h1>
  <p style="color:#666;margin:0;">Explore 20 years of crop yield, weather, and soil data across all 38 Tamil Nadu districts.</p>
</div>
""", unsafe_allow_html=True)

# ─── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    data_dir = Path(__file__).parent.parent.parent / "data"
    eng_path  = data_dir / "processed" / "engineered_data.csv"
    raw_path  = data_dir / "raw" / "weather_data.csv"

    if not eng_path.exists():
        return None, None
    df = pd.read_csv(eng_path)
    weather_df = pd.read_csv(raw_path) if raw_path.exists() else None
    return df, weather_df

df, weather_df = load_data()

if df is None:
    st.error("❌ Processed data not found. Please run `python setup.py` first.")
    st.stop()

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:20px 16px 12px;">
        <div style="font-size:2rem;margin-bottom:8px;">🌾</div>
        <div style="color:white;font-size:1.1rem;font-weight:700;font-family:'DM Serif Display',serif;">TN Crop Advisory</div>
        <div style="color:rgba(255,255,255,0.5);font-size:0.78rem;margin-top:4px;">AI · XGBoost · SHAP</div>
    </div>
    <div style="height:1px;background:rgba(255,255,255,0.1);margin:0 16px 12px;"></div>
    """, unsafe_allow_html=True)
    st.markdown("**Filters**")
    sel_districts = st.multiselect(
        "Select Districts (up to 5)",
        sorted(DISTRICTS.keys()),
        default=["Thanjavur", "Coimbatore", "Madurai"]
    )
    if len(sel_districts) > 5:
        st.warning("Max 5 districts.")
        sel_districts = sel_districts[:5]

    sel_crop = st.selectbox("Select Crop", CROPS, index=0)
    sel_season = st.selectbox("Select Season", ["All"] + SEASONS)

# ─── Filter Data ───────────────────────────────────────────────────────────────
df_filt = df[df["crop"] == sel_crop].copy()
if sel_season != "All":
    df_filt = df_filt[df_filt["season"] == sel_season]

if sel_districts:
    df_dist = df_filt[df_filt["district"].isin(sel_districts)]
else:
    df_dist = df_filt

if df_dist.empty:
    st.warning("No data found for the selected filters.")
    st.stop()

# ─── Overview Metrics ──────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📊 Overview Statistics")
col1, col2, col3, col4 = st.columns(4)

overall_avg = df_filt["yield_t_ha"].mean()
overall_max = df_filt["yield_t_ha"].max()
best_dist   = df_filt.groupby("district")["yield_t_ha"].mean().idxmax()
recent      = df_filt[df_filt["year"] >= 2020]["yield_t_ha"].mean()
old         = df_filt[df_filt["year"] < 2010]["yield_t_ha"].mean()
trend_delta = ((recent - old) / old * 100) if old > 0 else 0

with col1:
    st.metric("State-wide Avg Yield", f"{overall_avg:.2f} t/ha", f"{sel_crop}")
with col2:
    st.metric("Peak Yield Recorded", f"{overall_max:.2f} t/ha")
with col3:
    st.metric("Top Performing District", best_dist)
with col4:
    st.metric("20-Year Trend", f"{trend_delta:+.1f}%", "vs early 2000s")

st.markdown("---")

# ─── Chart 1: Yield Over Time ──────────────────────────────────────────────────
st.markdown("### 1️⃣ Yield Trend Over Time (Selected Districts)")

yearly_yield = (
    df_dist.groupby(["year", "district"])["yield_t_ha"]
    .mean()
    .reset_index()
)

palette = ["#2D6A2A", "#D4A373", "#D9534F", "#4A90D9", "#8E44AD"]

fig_trend = go.Figure()
for i, dist in enumerate(sel_districts):
    d = yearly_yield[yearly_yield["district"] == dist]
    color = palette[i % len(palette)]
    fig_trend.add_trace(go.Scatter(
        x=d["year"], y=d["yield_t_ha"],
        mode="lines+markers",
        name=dist,
        line=dict(color=color, width=2.5),
        marker=dict(size=6),
        hovertemplate=f"<b>{dist}</b><br>Year: %{{x}}<br>Yield: %{{y:.2f}} t/ha<extra></extra>"
    ))
    # Add trendline
    if len(d) > 2:
        z = np.polyfit(d["year"], d["yield_t_ha"], 1)
        p = np.poly1d(z)
        fig_trend.add_trace(go.Scatter(
            x=d["year"], y=p(d["year"]),
            mode="lines",
            name=f"{dist} Trend",
            line=dict(color=color, width=1, dash="dot"),
            showlegend=False,
            hoverinfo="skip"
        ))

fig_trend.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#333"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis=dict(title="Year", showgrid=True, gridcolor="#e8e3d8"),
    yaxis=dict(title="Yield (t/ha)", showgrid=True, gridcolor="#e8e3d8"),
    height=420,
    margin=dict(l=20, r=20, t=30, b=20)
)
st.plotly_chart(fig_trend, use_container_width=True)

# ─── Chart 2: Rainfall vs Yield Correlation ────────────────────────────────────
st.markdown("### 2️⃣ Rainfall vs. Yield Correlation")

scatter_data = df_dist[["district", "year", "rainfall_mm", "yield_t_ha"]].dropna()
fig_scatter = px.scatter(
    scatter_data,
    x="rainfall_mm", y="yield_t_ha",
    color="district",
    trendline="ols",
    color_discrete_sequence=palette,
    labels={"rainfall_mm": "Annual Rainfall (mm)", "yield_t_ha": "Yield (t/ha)"},
    hover_data=["year"]
)
fig_scatter.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#333"),
    height=400,
    margin=dict(l=20, r=20, t=30, b=20)
)
st.plotly_chart(fig_scatter, use_container_width=True)

# ─── Chart 3: Soil Fertility Trend ────────────────────────────────────────────
st.markdown("### 3️⃣ Soil Fertility Score Trend")
soil_trend = (
    df_dist.groupby(["year", "district"])["soil_fertility_score"]
    .mean()
    .reset_index()
)

fig_soil = px.line(
    soil_trend, x="year", y="soil_fertility_score",
    color="district",
    color_discrete_sequence=palette,
    labels={"soil_fertility_score": "Soil Fertility Score", "year": "Year"},
    markers=True
)
fig_soil.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#333"),
    height=380,
    margin=dict(l=20, r=20, t=30, b=20)
)
st.plotly_chart(fig_soil, use_container_width=True)

# ─── Chart 4: Season-wise Box Plot ─────────────────────────────────────────────
st.markdown("### 4️⃣ Season-wise Yield Distribution (All Districts)")
box_data = df[df["crop"] == sel_crop].copy()
fig_box = px.box(
    box_data, x="season", y="yield_t_ha",
    color="season",
    color_discrete_map={"Kharif": "#2D6A2A", "Rabi": "#D4A373", "Zaid": "#4A90D9"},
    labels={"yield_t_ha": "Yield (t/ha)", "season": "Season"},
    points="outliers"
)
fig_box.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#333"),
    showlegend=False,
    height=380,
    margin=dict(l=20, r=20, t=30, b=20)
)
st.plotly_chart(fig_box, use_container_width=True)

# ─── Chart 5: Statewide Temperature Trend ─────────────────────────────────────
if weather_df is not None:
    st.markdown("### 5️⃣ Tamil Nadu Average Temperature Trend (2003-2023)")
    temp_trend = weather_df.groupby("year")["temp_avg_c"].mean().reset_index()

    fig_temp = go.Figure()
    fig_temp.add_trace(go.Scatter(
        x=temp_trend["year"], y=temp_trend["temp_avg_c"],
        mode="lines+markers",
        fill="tozeroy",
        fillcolor="rgba(209,76,62,0.12)",
        line=dict(color="#D9534F", width=2.5),
        marker=dict(size=6, color="#D9534F"),
        name="Avg Temp (°C)"
    ))
    # Trendline
    z = np.polyfit(temp_trend["year"], temp_trend["temp_avg_c"], 1)
    p = np.poly1d(z)
    fig_temp.add_trace(go.Scatter(
        x=temp_trend["year"], y=p(temp_trend["year"]),
        mode="lines",
        line=dict(color="#1A1A2E", width=1.5, dash="dash"),
        name="Linear Trend"
    ))
    fig_temp.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans, sans-serif", color="#333"),
        yaxis=dict(title="Temperature (C)"),
        xaxis=dict(title="Year"),
        height=360,
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig_temp, use_container_width=True)

# ─── Raw Data Table ────────────────────────────────────────────────────────────
with st.expander("📋 View Raw Data Table"):
    cols_to_show = ["district", "year", "season", "yield_t_ha",
                    "rainfall_mm", "temp_avg_c", "soil_fertility_score", "fertilizer_kg_ha"]
    show_df = df_dist[cols_to_show].sort_values(["district","year"], ascending=[True,False])
    st.dataframe(show_df.style.format({
        "yield_t_ha": "{:.3f}",
        "rainfall_mm": "{:.1f}",
        "temp_avg_c": "{:.2f}",
        "soil_fertility_score": "{:.3f}",
        "fertilizer_kg_ha": "{:.1f}"
    }), use_container_width=True)
