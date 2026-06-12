"""
TN Crop Yield Advisory — Streamlit Dashboard Home
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="TN Crop Yield Advisory",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Minimal style injection (no large HTML blocks) ─────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #071407; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
.block-container { padding-top: 2rem !important; padding-bottom: 2rem !important; }

/* Sidebar */
[data-testid="stSidebar"] { background: #0c2210 !important; }
[data-testid="stSidebarNav"] a { color: rgba(255,255,255,.7) !important; border-radius: 8px; padding: 8px 12px; font-size:.9rem; font-weight:500; }
[data-testid="stSidebarNav"] a:hover,
[data-testid="stSidebarNav"] a[aria-current="page"] { background: rgba(65,176,65,.15) !important; color: #72d472 !important; }
[data-testid="stSidebarNav"] span { color: inherit !important; }

/* Metrics */
[data-testid="metric-container"] {
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.09);
    border-radius: 14px; padding: 20px 18px;
}
[data-testid="stMetricValue"] { color: #72d472 !important; font-size: 2rem !important; font-weight: 800 !important; }
[data-testid="stMetricLabel"] { color: rgba(255,255,255,.55) !important; font-size: .82rem !important; }
[data-testid="stMetricDelta"] { font-size: .8rem !important; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg,#287a26,#41b041);
    color: white; border: none; border-radius: 50px;
    padding: 10px 26px; font-weight: 700; font-size: .92rem;
    box-shadow: 0 4px 18px rgba(65,176,65,.3); transition: all .25s;
}
.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 8px 28px rgba(65,176,65,.5); }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background: rgba(255,255,255,.05); border-radius: 12px; padding: 4px; border: 1px solid rgba(255,255,255,.07); }
.stTabs [data-baseweb="tab"] { border-radius: 9px; padding: 8px 20px; font-weight: 500; color: rgba(255,255,255,.5); }
.stTabs [aria-selected="true"] { background: rgba(65,176,65,.15) !important; color: #72d472 !important; }

/* Inputs */
.stSelectbox [data-baseweb="select"] > div { background: rgba(255,255,255,.06); border-color: rgba(255,255,255,.14); border-radius: 10px; }
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:24px 16px 12px;">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
        <div style="width:36px;height:36px;border-radius:9px;background:linear-gradient(135deg,#287a26,#41b041);
                    display:flex;align-items:center;justify-content:center;font-size:1.1rem;flex-shrink:0;">🌾</div>
        <div>
          <div style="color:#fff;font-size:.95rem;font-weight:700;line-height:1.1;">TN Crop Advisory</div>
          <div style="color:rgba(255,255,255,.4);font-size:.65rem;letter-spacing:1.2px;text-transform:uppercase;">AI · XGBoost · SHAP</div>
        </div>
      </div>
      <div style="height:1px;background:linear-gradient(90deg,rgba(65,176,65,.5),transparent);margin-top:6px;"></div>
    </div>
    """, unsafe_allow_html=True)

# ── Load Data ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    p = Path(__file__).parent.parent / "data" / "processed" / "engineered_data.csv"
    return pd.read_csv(p) if p.exists() else None

df = load_data()

# ══════════════════════════════════════════════════════════════════════════════
# HERO BANNER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="
  background: linear-gradient(135deg, #0c2a10 0%, #163e1a 50%, #1f5222 100%);
  border: 1px solid rgba(65,176,65,0.2);
  border-radius: 20px;
  padding: 48px 44px 44px;
  margin-bottom: 32px;
  position: relative;
  overflow: hidden;
">
  <div style="position:absolute;top:-60px;right:-60px;width:280px;height:280px;
              border-radius:50%;background:radial-gradient(circle,rgba(65,176,65,.12),transparent 70%);
              pointer-events:none;"></div>
  <div style="position:absolute;bottom:-40px;left:30%;width:200px;height:200px;
              border-radius:50%;background:radial-gradient(circle,rgba(65,176,65,.07),transparent 70%);
              pointer-events:none;"></div>
  <div style="position:relative;z-index:1;">
    <div style="display:inline-flex;align-items:center;gap:8px;
                background:rgba(65,176,65,.12);border:1px solid rgba(65,176,65,.3);
                border-radius:50px;padding:6px 16px;margin-bottom:20px;">
      <div style="width:7px;height:7px;background:#41b041;border-radius:50%;"></div>
      <span style="font-size:.72rem;font-weight:700;color:#72d472;letter-spacing:1.6px;text-transform:uppercase;">
        AI-Powered Agricultural Intelligence
      </span>
    </div>
    <h1 style="font-family:'Playfair Display',serif;font-size:2.6rem;font-weight:800;
               color:#fff;line-height:1.1;margin-bottom:14px;">
      Tamil Nadu Crop Yield<br>
      <span style="background:linear-gradient(120deg,#80e680,#c5f0a0,#41b041);
                   background-size:200% auto;
                   -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
        Advisory System
      </span>
    </h1>
    <p style="color:rgba(255,255,255,.68);font-size:1rem;line-height:1.75;max-width:680px;margin:0;">
      Predict district-level crop yields, understand <em>why</em> using SHAP explainability,
      explore 20 years of climate &amp; soil data, and download personalised advisory PDF reports —
      all in one place.
    </p>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# METRICS ROW
# ══════════════════════════════════════════════════════════════════════════════
c1, c2, c3, c4, c5 = st.columns(5)
with c1: st.metric("Districts", "38", "All of TN")
with c2: st.metric("Crops", "6", "Major varieties")
with c3: st.metric("ML Models", "4", "LR · RF · XGB · LSTM")
with c4:
    rec = f"{len(df):,}" if df is not None else "—"
    st.metric("Training Records", rec, "20 years")
with c5: st.metric("Data Years", "21", "2003 – 2023")

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# CHARTS
# ══════════════════════════════════════════════════════════════════════════════
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="rgba(255,255,255,.7)"),
    margin=dict(l=0, r=10, t=24, b=0),
)

if df is not None:
    st.markdown("### 📊 Dataset Overview")
    col_l, col_r = st.columns(2, gap="large")

    with col_l:
        st.markdown("##### 🌿 Average Yield by Crop")
        crop_avg = (df.groupby("crop")["yield_t_ha"].mean()
                      .reset_index()
                      .sort_values("yield_t_ha"))
        fig = px.bar(
            crop_avg, x="yield_t_ha", y="crop", orientation="h",
            color="yield_t_ha",
            color_continuous_scale=["#163e1a", "#41b041"],
            labels={"yield_t_ha": "Avg Yield (t/ha)", "crop": ""},
            text=crop_avg["yield_t_ha"].apply(lambda v: f"{v:.1f}")
        )
        fig.update_traces(textposition="outside", marker_line_width=0,
                          textfont=dict(color="rgba(255,255,255,.8)"))
        fig.update_layout(**CHART_LAYOUT, coloraxis_showscale=False, height=300,
                          xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,.06)", zeroline=False),
                          yaxis=dict(showgrid=False))
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown("##### 📈 Statewide Yield Trend (2003–2023)")
        yr = df.groupby("year")["yield_t_ha"].mean().reset_index()
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=yr["year"], y=yr["yield_t_ha"],
            mode="lines+markers",
            fill="tozeroy", fillcolor="rgba(65,176,65,.07)",
            line=dict(color="#41b041", width=2.5),
            marker=dict(size=7, color="#41b041", line=dict(color="#071407", width=1.5)),
            hovertemplate="Year: %{x}<br>Yield: %{y:.2f} t/ha<extra></extra>"
        ))
        fig2.update_layout(
            **CHART_LAYOUT, height=300,
            xaxis=dict(title="Year", showgrid=True, gridcolor="rgba(255,255,255,.06)", zeroline=False),
            yaxis=dict(title="t/ha", showgrid=True, gridcolor="rgba(255,255,255,.06)")
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("##### 🏆 Top 10 Districts by Average Yield")
    top = df.groupby("district")["yield_t_ha"].mean().nlargest(10).reset_index()
    fig3 = px.bar(
        top, x="district", y="yield_t_ha",
        color="yield_t_ha",
        color_continuous_scale=["#163e1a", "#72d472"],
        labels={"yield_t_ha": "Avg Yield (t/ha)", "district": ""},
        text=top["yield_t_ha"].apply(lambda v: f"{v:.1f}")
    )
    fig3.update_traces(textposition="outside", marker_line_width=0,
                       textfont=dict(color="rgba(255,255,255,.8)"))
    fig3.update_layout(**CHART_LAYOUT, coloraxis_showscale=False, height=360,
                       xaxis=dict(showgrid=False),
                       yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,.06)"))
    st.plotly_chart(fig3, use_container_width=True)

else:
    st.info("ℹ️ No processed dataset found. Run the data pipeline to generate `data/processed/engineered_data.csv`.")

# ══════════════════════════════════════════════════════════════════════════════
# NAVIGATE CARDS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
st.markdown("### 🗂️ Navigate the System")

# Extra style for link buttons inside cards
st.markdown("""
<style>
.nav-card-wrap a[data-testid="stPageLink-NavLink"] {
    background: rgba(255,255,255,.08) !important;
    border-radius: 8px !important;
    padding: 6px 14px !important;
    font-size: .8rem !important;
    font-weight: 600 !important;
    margin-top: 12px !important;
    display: inline-block !important;
    transition: background .2s !important;
}
.nav-card-wrap a[data-testid="stPageLink-NavLink"]:hover {
    background: rgba(255,255,255,.15) !important;
}
</style>
""", unsafe_allow_html=True)

cards = [
    ("🔮", "Prediction",  "#41b041", "pages/01_Prediction.py",
     "Select district, crop & season → XGBoost yield forecast + SHAP factor chart."),
    ("🗺️", "Heatmap",    "#4a96dc", "pages/02_Heatmap.py",
     "Interactive map showing predicted yield potential across all 38 districts."),
    ("📋", "Advisory",   "#c9a032", "pages/03_Advisory.py",
     "Download a personalised PDF report with action plan based on your prediction."),
    ("📈", "Trends",     "#41b041", "pages/04_Trends.py",
     "Explore 20 years of yield, rainfall, soil & temperature data interactively."),
    ("⚖️", "Compare",   "#4a96dc", "pages/05_Compare.py",
     "Side-by-side district & crop comparison with radar, violin & bump charts."),
]

cols = st.columns(5)
for col, (icon, title, color, page, desc) in zip(cols, cards):
    with col:
        st.markdown(f"""
        <div style="
          background:rgba(255,255,255,.04);
          border:1px solid rgba(255,255,255,.08);
          border-top:3px solid {color};
          border-radius:16px;padding:22px 18px 14px;
          height:100%;
        ">
          <div style="font-size:1.7rem;margin-bottom:10px;">{icon}</div>
          <div style="font-weight:700;color:#fff;font-size:.95rem;margin-bottom:7px;">{title}</div>
          <div style="color:rgba(255,255,255,.52);font-size:.82rem;line-height:1.55;margin-bottom:14px;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
        st.page_link(page, label=f"Open {title} →", use_container_width=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;color:rgba(255,255,255,.25);font-size:.78rem;padding:40px 0 8px;">
  TN Crop Advisory System &nbsp;·&nbsp; Data: NASA POWER · Soil Health Card Portal &nbsp;·&nbsp;
  ML: XGBoost · SHAP · LSTM
</div>
""", unsafe_allow_html=True)
