# Tamil Nadu Crop Yield Advisory -- Exploratory Data Analysis
# ============================================================
# Run: python notebooks/eda_analysis.py
# Outputs are saved to reports/eda_outputs/

import sys
from pathlib import Path

# Fix: set ROOT relative to this script's real location when called directly
ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT))

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # non-interactive backend for Windows
import matplotlib.pyplot as plt
import seaborn as sns

# -- Config -------------------------------------------------------------------
DATA_DIR   = ROOT / "data" / "processed"
RAW_DIR    = ROOT / "data" / "raw"
OUTPUT_DIR = ROOT / "reports" / "eda_outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.facecolor": "#FAFAF5",
    "figure.facecolor": "#F7F3E9",
    "axes.edgecolor": "#CCCCCC",
    "axes.labelcolor": "#1A1A2E",
    "text.color": "#1A1A2E",
    "xtick.color": "#1A1A2E",
    "ytick.color": "#1A1A2E",
    "axes.grid": True,
    "grid.color": "#E0D8C8",
    "grid.linestyle": "--",
    "grid.alpha": 0.7,
})

BRAND_GREEN = "#2D6A2A"
BRAND_GOLD  = "#D4A373"
BRAND_RED   = "#D9534F"
BRAND_BLUE  = "#4A90D9"

# -- Load Data ----------------------------------------------------------------
print("[*] Loading data...")
df = pd.read_csv(DATA_DIR / "engineered_data.csv")
weather_df = pd.read_csv(RAW_DIR / "weather_data.csv") if (RAW_DIR / "weather_data.csv").exists() else None

print(f"    Rows: {len(df):,}  |  Columns: {len(df.columns)}")
print(f"    Years: {df['year'].min()}-{df['year'].max()}")
print(f"    Districts: {df['district'].nunique()}  |  Crops: {df['crop'].nunique()}")

# =============================================================================
# FIGURE 1 -- Basic Statistics & Distributions
# =============================================================================
print("\n[1/4] Generating basic statistics charts...")

fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle("TN Crop Yield Advisory -- Basic Statistics", fontsize=18, fontweight="bold", y=1.01)

# 1a. Overall yield distribution
ax = axes[0, 0]
df["yield_t_ha"].hist(bins=50, color=BRAND_GREEN, alpha=0.8, ax=ax, edgecolor="none")
ax.axvline(df["yield_t_ha"].mean(), color=BRAND_RED, linestyle="--", linewidth=1.5,
           label=f"Mean: {df['yield_t_ha'].mean():.2f}")
ax.axvline(df["yield_t_ha"].median(), color=BRAND_GOLD, linestyle=":", linewidth=1.5,
           label=f"Median: {df['yield_t_ha'].median():.2f}")
ax.set_title("Overall Yield Distribution", fontweight="bold")
ax.set_xlabel("Yield (t/ha)")
ax.legend()

# 1b. Yield by crop (boxplot)
ax = axes[0, 1]
crops_order = df.groupby("crop")["yield_t_ha"].median().sort_values(ascending=False).index.tolist()
data_by_crop = [df[df["crop"] == c]["yield_t_ha"].values for c in crops_order]
bp = ax.boxplot(data_by_crop, labels=crops_order, patch_artist=True,
                medianprops=dict(color=BRAND_RED, linewidth=2))
colors = [BRAND_GREEN, BRAND_GOLD, BRAND_BLUE, "#8E44AD", "#E67E22", "#1ABC9C"]
for patch, color in zip(bp["boxes"], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.75)
ax.set_title("Yield Distribution by Crop", fontweight="bold")
ax.set_ylabel("Yield (t/ha)")
ax.set_xticklabels(crops_order, rotation=15, ha="right")

# 1c. Yield by season
ax = axes[0, 2]
season_means = df.groupby("season")["yield_t_ha"].mean()
bars = ax.bar(season_means.index, season_means.values,
              color=[BRAND_GREEN, BRAND_GOLD, BRAND_BLUE], alpha=0.85, edgecolor="none")
for bar in bars:
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
            f"{bar.get_height():.2f}", ha="center", fontweight="bold")
ax.set_title("Average Yield by Season", fontweight="bold")
ax.set_ylabel("Avg Yield (t/ha)")

# 1d. Rainfall histogram
ax = axes[1, 0]
df["rainfall_mm"].hist(bins=40, color=BRAND_BLUE, alpha=0.8, ax=ax, edgecolor="none")
ax.set_title("Annual Rainfall Distribution", fontweight="bold")
ax.set_xlabel("Rainfall (mm)")

# 1e. Correlation heatmap
ax = axes[1, 1]
num_cols = ["yield_t_ha", "rainfall_mm", "temp_avg_c", "soil_N", "soil_P",
            "soil_K", "soil_pH", "soil_fertility_score", "fertilizer_kg_ha", "ndvi"]
corr = df[num_cols].corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, cmap="RdYlGn", center=0, ax=ax,
            annot=True, fmt=".2f", annot_kws={"size": 7},
            linewidths=0.4, square=False, cbar_kws={"shrink": 0.75})
ax.set_title("Feature Correlation Matrix", fontweight="bold")
ax.tick_params(axis="x", labelsize=8, rotation=45)
ax.tick_params(axis="y", labelsize=8, rotation=0)

# 1f. Yield trend for 3 selected crops
ax = axes[1, 2]
for crop, color in zip(["Rice", "Maize", "Groundnut"], [BRAND_GREEN, BRAND_GOLD, BRAND_RED]):
    y = df[df["crop"] == crop].groupby("year")["yield_t_ha"].mean()
    ax.plot(y.index, y.values, color=color, linewidth=2, label=crop, marker="o", markersize=4)
ax.set_title("Yield Trend (Selected Crops)", fontweight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("Avg Yield (t/ha)")
ax.legend()

plt.tight_layout()
out1 = OUTPUT_DIR / "01_basic_statistics.png"
plt.savefig(out1, dpi=150, bbox_inches="tight")
print(f"    Saved -> {out1}")
plt.close()


# =============================================================================
# FIGURE 2 -- Top/Bottom Districts per Crop
# =============================================================================
print("[2/4] Generating district performance charts...")

crops = df["crop"].unique().tolist()
fig, axes = plt.subplots(len(crops), 2, figsize=(20, len(crops) * 4))
fig.suptitle("Top & Bottom 5 Districts by Crop (Average Yield)", fontsize=16, fontweight="bold")

for i, crop in enumerate(crops):
    sub = df[df["crop"] == crop].groupby("district")["yield_t_ha"].mean().sort_values()
    bottom5 = sub.head(5)
    top5    = sub.tail(5)

    ax_l = axes[i, 0]
    ax_r = axes[i, 1]

    bottom5.plot(kind="barh", ax=ax_l, color=BRAND_RED, alpha=0.8, edgecolor="none")
    ax_l.set_title(f"{crop} -- Bottom 5 Districts", fontweight="bold")
    ax_l.set_xlabel("Avg Yield (t/ha)")
    for j, v in enumerate(bottom5.values):
        ax_l.text(v + 0.01, j, f"{v:.2f}", va="center", fontsize=9)

    top5.plot(kind="barh", ax=ax_r, color=BRAND_GREEN, alpha=0.8, edgecolor="none")
    ax_r.set_title(f"{crop} -- Top 5 Districts", fontweight="bold")
    ax_r.set_xlabel("Avg Yield (t/ha)")
    for j, v in enumerate(top5.values):
        ax_r.text(v + 0.01, j, f"{v:.2f}", va="center", fontsize=9)

plt.tight_layout()
out2 = OUTPUT_DIR / "02_district_performance.png"
plt.savefig(out2, dpi=150, bbox_inches="tight")
print(f"    Saved -> {out2}")
plt.close()


# =============================================================================
# FIGURE 3 -- Climate Trends
# =============================================================================
print("[3/4] Generating climate trend charts...")

if weather_df is not None:
    fig, axes = plt.subplots(1, 2, figsize=(16, 5))
    fig.suptitle("Tamil Nadu Climate Trends (2003-2023)", fontsize=16, fontweight="bold")

    # Rainfall trend
    ax = axes[0]
    rain = weather_df.groupby("year")["rainfall_mm"].agg(["mean", "std"]).reset_index()
    ax.fill_between(rain["year"], rain["mean"] - rain["std"], rain["mean"] + rain["std"],
                    alpha=0.2, color=BRAND_BLUE)
    ax.plot(rain["year"], rain["mean"], color=BRAND_BLUE, linewidth=2.5, marker="o", markersize=5)
    z = np.polyfit(rain["year"], rain["mean"], 1)
    ax.plot(rain["year"], np.poly1d(z)(rain["year"]), linestyle="--", color="#1A1A2E", linewidth=1.5,
            label=f"Trend: {z[0]:+.1f} mm/yr")
    ax.set_title("Statewide Average Rainfall", fontweight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel("Rainfall (mm)")
    ax.legend()

    # Temperature trend
    ax = axes[1]
    temp = weather_df.groupby("year")["temp_avg_c"].agg(["mean", "std"]).reset_index()
    ax.fill_between(temp["year"], temp["mean"] - temp["std"], temp["mean"] + temp["std"],
                    alpha=0.15, color=BRAND_RED)
    ax.plot(temp["year"], temp["mean"], color=BRAND_RED, linewidth=2.5, marker="o", markersize=5)
    z2 = np.polyfit(temp["year"], temp["mean"], 1)
    ax.plot(temp["year"], np.poly1d(z2)(temp["year"]), linestyle="--", color="#1A1A2E", linewidth=1.5,
            label=f"Trend: {z2[0]*10:+.3f} C/decade")
    ax.set_title("Statewide Average Temperature", fontweight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel("Temperature (C)")
    ax.legend()

    plt.tight_layout()
    out3 = OUTPUT_DIR / "03_climate_trends.png"
    plt.savefig(out3, dpi=150, bbox_inches="tight")
    print(f"    Saved -> {out3}")
    plt.close()
else:
    print("    Skipped (weather_data.csv not found)")


# =============================================================================
# FIGURE 4 -- Soil Health Profile
# =============================================================================
print("[4/4] Generating soil health charts...")

from utils.district_coords import DISTRICTS as DC
df["zone"] = df["district"].map(lambda d: DC.get(d, {}).get("zone", "Unknown"))

fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle("Soil Health Profile by Zone", fontsize=16, fontweight="bold")

zones = sorted(df["zone"].dropna().unique().tolist())

# N by zone
ax = axes[0, 0]
n_vals = [df[df["zone"] == z]["soil_N"].dropna().values for z in zones]
bp = ax.boxplot(n_vals, labels=zones, patch_artist=True,
                medianprops=dict(color=BRAND_RED, linewidth=2))
for p in bp["boxes"]:
    p.set_facecolor(BRAND_GREEN)
    p.set_alpha(0.7)
ax.set_title("Soil Nitrogen (N) by Zone", fontweight="bold")
ax.set_ylabel("N (kg/ha)")

# P by zone
ax = axes[0, 1]
p_vals = [df[df["zone"] == z]["soil_P"].dropna().values for z in zones]
bp2 = ax.boxplot(p_vals, labels=zones, patch_artist=True,
                 medianprops=dict(color=BRAND_RED, linewidth=2))
for p in bp2["boxes"]:
    p.set_facecolor(BRAND_GOLD)
    p.set_alpha(0.7)
ax.set_title("Soil Phosphorus (P) by Zone", fontweight="bold")
ax.set_ylabel("P (kg/ha)")

# pH distribution
ax = axes[1, 0]
zone_colors = [BRAND_GREEN, BRAND_GOLD, BRAND_BLUE, BRAND_RED, "#8E44AD"]
for zone, color in zip(zones, zone_colors):
    vals = df[df["zone"] == zone]["soil_pH"].dropna()
    ax.hist(vals, bins=20, alpha=0.5, label=zone, color=color, edgecolor="none")
ax.axvline(6.8, linestyle="--", color="#1A1A2E", linewidth=1.5, label="Optimal pH 6.8")
ax.set_title("Soil pH Distribution by Zone", fontweight="bold")
ax.set_xlabel("pH")
ax.legend(fontsize=8)

# Fertility score by crop
ax = axes[1, 1]
crop_list = sorted(df["crop"].unique().tolist())
fert_vals = [df[df["crop"] == c]["soil_fertility_score"].dropna().values for c in crop_list]
bp3 = ax.boxplot(fert_vals, labels=crop_list, patch_artist=True,
                 medianprops=dict(color=BRAND_RED, linewidth=2))
for p, color in zip(bp3["boxes"], zone_colors):
    p.set_facecolor(color)
    p.set_alpha(0.7)
ax.set_title("Soil Fertility Score by Crop", fontweight="bold")
ax.set_ylabel("Fertility Score")
ax.tick_params(axis="x", rotation=15)

plt.tight_layout()
out4 = OUTPUT_DIR / "04_soil_health.png"
plt.savefig(out4, dpi=150, bbox_inches="tight")
print(f"    Saved -> {out4}")
plt.close()


# -- Summary Stats ------------------------------------------------------------
print("\n--- Summary Statistics (Yield by Crop) ---")
print(df.groupby("crop")["yield_t_ha"].describe().round(3).to_string())

print("\n--- Correlation with Yield ---")
print(df[["yield_t_ha", "rainfall_mm", "temp_avg_c", "soil_N",
          "soil_fertility_score", "fertilizer_kg_ha", "ndvi"]].corr()["yield_t_ha"].round(3).to_string())

print(f"\n[DONE] All 4 chart sets saved to: {OUTPUT_DIR}")
