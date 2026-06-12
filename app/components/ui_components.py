"""
Reusable Streamlit UI components for the TN Crop Advisory System.
Import these in any page for consistent styling.
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

BRAND_GREEN = "#2D6A2A"
BRAND_GOLD  = "#D4A373"
BG_COLOR    = "#F7F3E9"
TEXT_COLOR  = "#1A1A2E"


def inject_global_css():
    """Inject the shared global CSS into any page."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        * { font-family: 'Inter', sans-serif; }
        .stApp { background-color: #F7F3E9; }
        h1, h2, h3 { color: #1A1A2E; }
        h1 { border-bottom: 3px solid #2D6A2A; padding-bottom: 10px; }
        .stButton>button {
            background: linear-gradient(135deg, #2D6A2A, #4CAF50);
            color: white; border-radius: 10px; border: none;
            padding: 12px 28px; font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 14px rgba(45,106,42,0.3);
        }
        .stButton>button:hover {
            box-shadow: 0 6px 20px rgba(45,106,42,0.45);
            transform: translateY(-2px);
        }
        [data-testid="stMetricValue"] { color: #2D6A2A; font-size: 2rem; font-weight: 700; }
        [data-testid="metric-container"] {
            background: white; border-radius: 12px; padding: 16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.07); border-top: 3px solid #2D6A2A;
        }
    </style>
    """, unsafe_allow_html=True)


def info_card(title: str, body: str, border_color: str = BRAND_GREEN):
    """Render a styled info card."""
    st.markdown(f"""
    <div style="
        background: white; border-radius: 12px; padding: 20px;
        border-left: 5px solid {border_color};
        box-shadow: 0 4px 12px rgba(0,0,0,0.07); margin-bottom: 16px;">
        <h4 style="color: {border_color}; margin: 0 0 8px 0;">{title}</h4>
        <p style="color: #555; margin: 0; line-height: 1.6;">{body}</p>
    </div>
    """, unsafe_allow_html=True)


def page_header(icon: str, title: str, subtitle: str = ""):
    """Render a consistent page header."""
    st.markdown(f"""
    <div style="margin-bottom: 24px;">
        <h1>{icon} {title}</h1>
        {"<p style='color:#555; font-size:1.05rem; margin-top:-8px;'>" + subtitle + "</p>" if subtitle else ""}
    </div>
    """, unsafe_allow_html=True)


def yield_gauge(value: float, avg: float, label: str = "Predicted Yield"):
    """Render a Plotly gauge chart for yield prediction result."""
    max_val = avg * 2.5 if avg > 0 else 10.0
    color = "#2D6A2A" if value >= avg else ("#F0AD4E" if value >= avg * 0.85 else "#D9534F")

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        delta={"reference": avg, "valueformat": ".2f", "suffix": " t/ha vs avg"},
        number={"suffix": " t/ha", "valueformat": ".2f", "font": {"size": 36, "color": color}},
        title={"text": label, "font": {"size": 16, "color": TEXT_COLOR}},
        gauge={
            "axis": {"range": [0, max_val], "ticksuffix": " t/ha"},
            "bar": {"color": color},
            "bgcolor": "white",
            "borderwidth": 2,
            "bordercolor": "#E0D8C8",
            "steps": [
                {"range": [0, avg * 0.85], "color": "rgba(217,83,79,0.1)"},
                {"range": [avg * 0.85, avg * 1.05], "color": "rgba(240,173,78,0.1)"},
                {"range": [avg * 1.05, max_val], "color": "rgba(45,106,42,0.1)"},
            ],
            "threshold": {
                "line": {"color": "#1A1A2E", "width": 2},
                "thickness": 0.75,
                "value": avg
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor="#F7F3E9",
        height=280,
        margin=dict(l=20, r=20, t=20, b=20),
        font=dict(family="Inter, sans-serif")
    )
    return fig


def status_badge(value: float, avg: float) -> str:
    """Return an HTML status badge based on yield vs average."""
    diff = value - avg
    if diff > 0.5:
        return '<span style="background:#2D6A2A;color:white;padding:4px 12px;border-radius:20px;font-weight:600;">🌟 Excellent</span>'
    elif diff >= 0:
        return '<span style="background:#4CAF50;color:white;padding:4px 12px;border-radius:20px;font-weight:600;">✅ Good</span>'
    elif diff >= -0.3:
        return '<span style="background:#F0AD4E;color:white;padding:4px 12px;border-radius:20px;font-weight:600;">⚠️ Average</span>'
    else:
        return '<span style="background:#D9534F;color:white;padding:4px 12px;border-radius:20px;font-weight:600;">🔴 Below Average</span>'


def sidebar_branding():
    """Inject branding into the sidebar."""
    st.sidebar.markdown("""
    <div style="text-align:center; padding: 10px 0 20px 0;">
        <div style="font-size: 2.5rem;">🌾</div>
        <div style="color: white; font-weight: 700; font-size: 1.05rem; line-height: 1.3;">
            TN Crop Advisory<br/>
            <span style="font-weight: 300; font-size: 0.85rem; opacity: 0.85;">AI-Powered Yield Intelligence</span>
        </div>
    </div>
    <hr style="border-color: rgba(255,255,255,0.2); margin: 0 0 16px 0;"/>
    """, unsafe_allow_html=True)
