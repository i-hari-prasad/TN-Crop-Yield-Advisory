"""
Advisory Page — Actionable recommendations + PDF report download.
"""
import streamlit as st
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from utils.pdf_generator import generate_advisory_pdf

st.set_page_config(page_title="Advisory | TN Crop Advisory", page_icon="📋", layout="wide")

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
    📋 Advisory Report
  </h1>
  <p style="color:#666;margin:0;">Personalised action plan based on your prediction. Download a PDF to share with extension officers.</p>
</div>
""", unsafe_allow_html=True)

# ── Check prediction ──────────────────────────────────────────────────────────
if 'last_prediction' not in st.session_state:
    st.markdown("""
    <div style="background:white;border-radius:14px;padding:32px;text-align:center;
         box-shadow:0 2px 10px rgba(0,0,0,0.06);">
      <div style="font-size:3rem;margin-bottom:12px;">🔮</div>
      <h3 style="color:#1c3a1c;margin-bottom:8px;">No Prediction Yet</h3>
      <p style="color:#666;">Please go to the <b>Prediction</b> page, fill in your farm details,<br>
      and click <b>Predict Yield</b> — then come back here.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

pred = st.session_state['last_prediction']
crop, district, season = pred['crop'], pred['district'], pred['season']
pred_yield, hist_avg = pred['yield_pred'], pred['district_avg']
diff = pred_yield - hist_avg

# ── Summary Banner ────────────────────────────────────────────────────────────
badge_clr = "#2d6a2a" if diff > 0.5 else ("#4caf50" if diff >= 0 else ("#f0ad4e" if diff >= -0.3 else "#d9534f"))
badge_txt = "Excellent" if diff > 0.5 else ("Good" if diff >= 0 else ("Average" if diff >= -0.3 else "Below Average"))

st.markdown(f"""
<div style="background:linear-gradient(135deg,#1c3a1c,#2d6a2a);border-radius:14px;
     padding:28px 32px;margin-bottom:24px;color:white;">
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;">
    <div>
      <div style="font-size:0.82rem;letter-spacing:1.5px;text-transform:uppercase;
           color:rgba(255,255,255,0.6);margin-bottom:6px;">Advisory for</div>
      <div style="font-size:1.4rem;font-weight:700;font-family:'DM Serif Display',serif;">
        {crop} · {district} · {season}
      </div>
    </div>
    <div style="text-align:right;">
      <div style="font-size:2.6rem;font-weight:800;line-height:1;">{pred_yield:.2f} t/ha</div>
      <div style="color:rgba(255,255,255,0.7);font-size:0.88rem;">
        {diff:+.2f} vs district avg ({hist_avg:.2f} t/ha)
      </div>
      <span style="background:{badge_clr};border:2px solid rgba(255,255,255,0.3);
            color:white;padding:4px 14px;border-radius:20px;font-size:0.82rem;
            font-weight:600;margin-top:6px;display:inline-block;">{badge_txt}</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Recommendations ───────────────────────────────────────────────────────────
top_factors = pred.get('top_factors', [])
input_data  = pred.get('input_data', None)

recs = []

# Factor-based recommendations
for factor in top_factors:
    name, impact = factor['name'], factor['impact']
    if "Fertilizer" in name:
        recs.append(("✅" if impact > 0 else "⚠️",
                      "Fertilizer Application",
                      "Current fertilizer rate is boosting yield." if impact > 0
                      else "Optimize NPK — consider soil testing to apply exact quantities needed."))
    elif any(n in name for n in ["Nitrogen","Phosphorus","Potassium","Fertility"]):
        if impact < 0:
            recs.append(("⚠️","Soil Nutrients",
                          "Low soil nutrients are limiting yield. Apply organic compost (FYM) before sowing."))
    elif "Rainfall" in name:
        recs.append(("💧" if impact < 0 else "🌧️",
                      "Rainfall / Irrigation",
                      "Consider drip/sprinkler irrigation to compensate for rainfall deficit." if impact < 0
                      else "Good rainfall contribution. Ensure proper drainage to prevent waterlogging."))
    elif "Temperature" in name and impact < 0:
        recs.append(("🌡️","Heat Stress",
                      "Adjust sowing date to avoid peak heat during critical flowering/grain filling stages."))
    elif "pH" in name and impact < 0 and input_data is not None:
        try:
            ph = input_data['soil_pH'].values[0]
            if ph < 6.0:
                recs.append(("🧪","Soil pH",f"Soil is acidic (pH {ph:.1f}). Apply agricultural lime before the next season."))
            elif ph > 7.5:
                recs.append(("🧪","Soil pH",f"Soil is alkaline (pH {ph:.1f}). Apply gypsum or organic matter to reduce pH."))
        except Exception:
            pass

# Default recs
if not recs:
    recs.append(("✅","General Conditions","Conditions are broadly favorable. Follow Good Agricultural Practices (GAP)."))

# Yield-based extra advice
if diff < -0.3:
    recs.insert(0, ("🔴","Low Yield Alert",
                     f"Predicted yield is {abs(diff):.2f} t/ha below district average. "
                     "Consider consulting local extension officers for targeted intervention."))
elif diff > 0.5:
    recs.insert(0, ("🌟","High Yield Potential",
                     "Conditions point to an above-average harvest. Ensure timely harvesting and post-harvest storage."))

# General always-on advice
recs += [
    ("📅","Sowing Window","Sow within the optimal 2-week window for your region to maximize radiation interception."),
    ("💊","Pest & Disease","Scout fields every 7 days. Use Integrated Pest Management (IPM) over chemical spraying."),
    ("🏪","Market Linkage","Register at the nearest APMC mandi at least 4 weeks before estimated harvest to secure fair prices."),
]

st.markdown("### Action Plan")
for icon, title, body in recs:
    st.markdown(f"""
    <div style="background:white;border-radius:12px;padding:18px 20px;margin-bottom:12px;
         box-shadow:0 2px 8px rgba(0,0,0,0.05);border-left:4px solid #2d6a2a;
         display:flex;gap:14px;align-items:flex-start;">
      <span style="font-size:1.5rem;line-height:1.3;">{icon}</span>
      <div>
        <div style="font-weight:700;color:#1c3a1c;margin-bottom:3px;">{title}</div>
        <div style="color:#555;font-size:0.9rem;line-height:1.5;">{body}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── PDF Download ──────────────────────────────────────────────────────────────
st.markdown("### Download PDF Report")
st.markdown("A printable A4 report for sharing with agricultural extension officers or government portals.")

reports_dir = Path(__file__).parent.parent.parent / "reports"
reports_dir.mkdir(exist_ok=True)
pdf_path = reports_dir / f"Advisory_{district}_{crop}_{season}.pdf".replace(" ", "_")

pred['recommendations'] = [f"{icon} {title}: {body}" for icon, title, body in recs]

if st.button("📄 Generate & Download PDF Report", type="primary", use_container_width=True):
    with st.spinner("Generating PDF..."):
        try:
            generate_advisory_pdf(pred, str(pdf_path))
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()
            st.download_button(
                label="⬇️ Download PDF",
                data=pdf_bytes,
                file_name=pdf_path.name,
                mime="application/pdf",
                use_container_width=True
            )
            st.success("PDF ready! Click the button above to download.")
        except Exception as e:
            st.error(f"PDF generation failed: {e}")
