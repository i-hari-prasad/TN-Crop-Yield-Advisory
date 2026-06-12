"""
District & Crop Comparison Page.
Side-by-side comparison of yield metrics across districts and crops using Plotly.
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
    page_title="Compare | TN Crop Advisory",
    page_icon="⚖️",
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
    ⚖️ District & Crop Comparison
  </h1>
  <p style="color:#666;margin:0;">Compare yield performance across multiple districts and crops side-by-side.</p>
</div>
""", unsafe_allow_html=True)

# ─── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    data_dir = Path(__file__).parent.parent.parent / "data" / "processed"
    path = data_dir / "engineered_data.csv"
    if not path.exists():
        return None
    return pd.read_csv(path)

df = load_data()
if df is None:
    st.error("❌ Processed data not found. Please run `python setup.py` first.")
    st.stop()

# ─── Mode Selection ────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🏘️ District vs District", "🌾 Crop vs Crop", "📅 Year-on-Year Rank"])

PALETTE = ["#2D6A2A", "#D4A373", "#D9534F", "#4A90D9", "#8E44AD", "#E67E22"]

# ══════════════════════════════════════════════════════════════════════
# TAB 1: District vs District
# ══════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("#### Compare up to 5 districts for a selected crop & season")
    col_a, col_b = st.columns(2)
    with col_a:
        crop_d = st.selectbox("Crop", CROPS, key="crop_dist")
    with col_b:
        season_d = st.selectbox("Season", ["All"] + SEASONS, key="season_dist")

    districts_d = st.multiselect(
        "Select Districts to Compare",
        sorted(DISTRICTS.keys()),
        default=["Thanjavur", "Coimbatore", "Madurai", "Vellore", "Erode"],
        key="dists"
    )

    if not districts_d:
        st.info("Please select at least one district.")
    else:
        # Filter
        df_d = df[df["crop"] == crop_d].copy()
        if season_d != "All":
            df_d = df_d[df_d["season"] == season_d]
        df_d = df_d[df_d["district"].isin(districts_d)]

        # Summary stats
        summary = df_d.groupby("district").agg(
            avg_yield=("yield_t_ha", "mean"),
            max_yield=("yield_t_ha", "max"),
            min_yield=("yield_t_ha", "min"),
            std_yield=("yield_t_ha", "std"),
            avg_rainfall=("rainfall_mm", "mean"),
            avg_temp=("temp_avg_c", "mean"),
            avg_fertility=("soil_fertility_score", "mean")
        ).reset_index().round(3)

        # --- Bar Chart: Average Yield
        st.markdown("##### 📊 Average Yield by District")
        fig_bar = px.bar(
            summary.sort_values("avg_yield", ascending=True),
            x="avg_yield", y="district",
            orientation="h",
            color="avg_yield",
            color_continuous_scale=["#D9534F", "#F0AD4E", "#2D6A2A"],
            labels={"avg_yield": "Avg Yield (t/ha)", "district": "District"},
            text=summary.sort_values("avg_yield", ascending=True)["avg_yield"].apply(lambda x: f"{x:.2f}")
        )
        fig_bar.update_traces(textposition="outside")
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Sans, sans-serif", color="#333"),
            coloraxis_showscale=False,
            height=max(300, len(districts_d) * 60),
            margin=dict(l=20, r=80, t=20, b=20)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # --- Radar Chart: Multi-metric Comparison
        st.markdown("##### 🕸️ Multi-Metric Radar Comparison")
        categories = ["Avg Yield", "Max Yield", "Avg Rainfall (÷100)", "Avg Temp", "Soil Fertility (×10)"]

        fig_radar = go.Figure()
        for i, dist in enumerate(districts_d):
            row = summary[summary["district"] == dist]
            if row.empty:
                continue
            row = row.iloc[0]
            values = [
                row["avg_yield"],
                row["max_yield"],
                row["avg_rainfall"] / 100,
                row["avg_temp"],
                row["avg_fertility"] * 10
            ]
            values += [values[0]]  # close loop
            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=categories + [categories[0]],
                fill="toself",
                name=dist,
                line=dict(color=PALETTE[i % len(PALETTE)], width=2),
                fillcolor=PALETTE[i % len(PALETTE)].replace("#", "rgba(").replace(")", ",0.12)") if False else PALETTE[i % len(PALETTE)],
                opacity=0.7
            ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, showgrid=True, gridcolor="#E0D8C8"),
                bgcolor="#FAFAF5"
            ),
            paper_bgcolor="#F7F3E9",
            font=dict(family="Inter, sans-serif", color="#1A1A2E"),
            height=450,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            margin=dict(l=40, r=40, t=40, b=80)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        # --- Yield Volatility
        st.markdown("##### 📉 Yield Volatility (Standard Deviation)")
        fig_vol = px.bar(
            summary.sort_values("std_yield", ascending=False),
            x="district", y="std_yield",
            color="std_yield",
            color_continuous_scale=["#2D6A2A", "#F0AD4E", "#D9534F"],
            labels={"std_yield": "Std Dev of Yield (t/ha)", "district": "District"},
            text=summary.sort_values("std_yield", ascending=False)["std_yield"].apply(lambda x: f"{x:.3f}")
        )
        fig_vol.update_traces(textposition="outside")
        fig_vol.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Sans, sans-serif", color="#333"),
            coloraxis_showscale=False,
            height=340,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_vol, use_container_width=True)

        # --- Summary Table
        st.markdown("##### 📋 Summary Table")
        display_summary = summary.rename(columns={
            "avg_yield": "Avg Yield (t/ha)",
            "max_yield": "Peak Yield (t/ha)",
            "min_yield": "Min Yield (t/ha)",
            "std_yield": "Std Dev",
            "avg_rainfall": "Avg Rainfall (mm)",
            "avg_temp": "Avg Temp (°C)",
            "avg_fertility": "Avg Fertility Score"
        })
        st.dataframe(
            display_summary.set_index("district").style.background_gradient(
                subset=["Avg Yield (t/ha)"], cmap="YlGn"
            ).format("{:.3f}"),
            use_container_width=True
        )

# ══════════════════════════════════════════════════════════════════════
# TAB 2: Crop vs Crop
# ══════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("#### Compare all crops or selected crops for a specific district")
    col_x, col_y = st.columns(2)
    with col_x:
        dist_c = st.selectbox("Select District", sorted(DISTRICTS.keys()), index=list(sorted(DISTRICTS.keys())).index("Thanjavur"), key="dist_crop")
    with col_y:
        season_c = st.selectbox("Season", ["All"] + SEASONS, key="season_crop")

    crops_c = st.multiselect("Select Crops", CROPS, default=CROPS, key="crops_sel")

    if not crops_c:
        st.info("Please select at least one crop.")
    else:
        df_c = df[df["district"] == dist_c].copy()
        if season_c != "All":
            df_c = df_c[df_c["season"] == season_c]
        df_c = df_c[df_c["crop"].isin(crops_c)]

        # Normalize yields to 0-100% for fair comparison
        crop_stats = df_c.groupby("crop").agg(
            avg_yield=("yield_t_ha", "mean"),
            max_yield=("yield_t_ha", "max"),
            trend_recent=("yield_t_ha", lambda x: x[df_c.loc[x.index, "year"] >= 2019].mean()),
            trend_old=("yield_t_ha", lambda x: x[df_c.loc[x.index, "year"] < 2010].mean())
        ).reset_index()
        crop_stats["growth_pct"] = (
            (crop_stats["trend_recent"] - crop_stats["trend_old"]) / crop_stats["trend_old"] * 100
        ).round(1)

        # Yield timeline per crop
        st.markdown("##### 📈 Crop Yield Over Time")
        yearly_crop = df_c.groupby(["year", "crop"])["yield_t_ha"].mean().reset_index()
        fig_crop_time = px.line(
            yearly_crop, x="year", y="yield_t_ha",
            color="crop",
            color_discrete_sequence=PALETTE,
            labels={"yield_t_ha": "Yield (t/ha)", "year": "Year", "crop": "Crop"},
            markers=True
        )
        fig_crop_time.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Sans, sans-serif", color="#333"),
            height=400,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_crop_time, use_container_width=True)

        # 20-yr growth rate
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown("##### 🚀 20-Year Growth Rate by Crop")
            fig_growth = px.bar(
                crop_stats.sort_values("growth_pct"),
                x="growth_pct", y="crop",
                orientation="h",
                color="growth_pct",
                color_continuous_scale=["#D9534F", "#F0AD4E", "#2D6A2A"],
                labels={"growth_pct": "Growth % (2019-23 vs 2003-09)", "crop": "Crop"},
                text=crop_stats.sort_values("growth_pct")["growth_pct"].apply(lambda x: f"{x:+.1f}%")
            )
            fig_growth.update_traces(textposition="outside")
            fig_growth.update_layout(
                paper_bgcolor="#F7F3E9", plot_bgcolor="#FAFAF5",
                font=dict(family="Inter, sans-serif", color="#1A1A2E"),
                coloraxis_showscale=False,
                height=320,
                margin=dict(l=20, r=70, t=20, b=20)
            )
            st.plotly_chart(fig_growth, use_container_width=True)

        with col_g2:
            st.markdown("##### 📊 Crop Stats Summary")
            st.dataframe(
                crop_stats.rename(columns={
                    "avg_yield": "Avg Yield (t/ha)",
                    "max_yield": "Peak Yield (t/ha)",
                    "growth_pct": "Growth %"
                })[["crop", "Avg Yield (t/ha)", "Peak Yield (t/ha)", "Growth %"]].set_index("crop"),
                use_container_width=True
            )

        # Violin plot for distribution
        st.markdown("##### 🎻 Yield Distribution by Crop")
        fig_violin = px.violin(
            df_c, y="yield_t_ha", x="crop",
            color="crop",
            color_discrete_sequence=PALETTE,
            box=True,
            points="outliers",
            labels={"yield_t_ha": "Yield (t/ha)", "crop": "Crop"}
        )
        fig_violin.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Sans, sans-serif", color="#333"),
            showlegend=False,
            height=380,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_violin, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════
# TAB 3: Year-on-Year Ranking
# ══════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("#### See how district rankings change over time for a given crop")
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        crop_r = st.selectbox("Crop", CROPS, key="crop_rank")
    with col_r2:
        top_n = st.slider("Show Top N Districts", 5, 15, 10)

    df_r = df[df["crop"] == crop_r].copy()
    yearly_rank = (
        df_r.groupby(["year", "district"])["yield_t_ha"]
        .mean()
        .reset_index()
    )
    yearly_rank["rank"] = yearly_rank.groupby("year")["yield_t_ha"].rank(ascending=False, method="min")

    # Get top_n districts by most recent year
    latest_year = yearly_rank["year"].max()
    top_dists = (
        yearly_rank[yearly_rank["year"] == latest_year]
        .nsmallest(top_n, "rank")["district"]
        .tolist()
    )

    yearly_rank_top = yearly_rank[yearly_rank["district"].isin(top_dists)]

    # Bump / rank chart
    st.markdown(f"##### 🏆 District Yield Rankings Over Time (Top {top_n} by latest year)")
    fig_bump = go.Figure()
    for i, dist in enumerate(top_dists):
        d = yearly_rank_top[yearly_rank_top["district"] == dist].sort_values("year")
        fig_bump.add_trace(go.Scatter(
            x=d["year"], y=d["rank"],
            mode="lines+markers+text",
            name=dist,
            line=dict(color=PALETTE[i % len(PALETTE)], width=2),
            marker=dict(size=8),
            text=d["year"].apply(lambda yr: dist if yr == latest_year else ""),
            textposition="middle right",
        ))

    fig_bump.update_yaxes(autorange="reversed", title="Rank (1 = Highest Yield)")
    fig_bump.update_xaxes(title="Year")
    fig_bump.update_layout(
        paper_bgcolor="#F7F3E9",
        plot_bgcolor="#FAFAF5",
        font=dict(family="Inter, sans-serif", color="#1A1A2E"),
        height=500,
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.01),
        margin=dict(l=20, r=160, t=20, b=20)
    )
    st.plotly_chart(fig_bump, use_container_width=True)

    # Heatmap: district vs year
    st.markdown("##### 🗓️ Yield Heatmap (District × Year)")
    pivot = yearly_rank[yearly_rank["district"].isin(top_dists)].pivot(
        index="district", columns="year", values="yield_t_ha"
    ).round(2)

    fig_heat = px.imshow(
        pivot,
        color_continuous_scale=["#D9534F", "#F0AD4E", "#2D6A2A"],
        labels=dict(color="Yield (t/ha)"),
        aspect="auto"
    )
    fig_heat.update_layout(
        paper_bgcolor="#F7F3E9",
        font=dict(family="Inter, sans-serif", color="#1A1A2E"),
        height=400,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig_heat, use_container_width=True)
