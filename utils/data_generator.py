"""
Realistic Synthetic Data Generator for TN Crop Yield Advisory System.
Generates 20 years of data for 38 districts × 6 crops with realistic correlations.
Also attempts to fetch real NASA POWER weather data (falls back to synthetic if offline).
"""

import numpy as np
import pandas as pd
import requests
import os
import time
from pathlib import Path

# Add parent dir to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.district_coords import (
    DISTRICTS, DISTRICT_NAMES, CROPS, SEASONS,
    CROP_YIELD_RANGES, CROP_SEASON_MAP,
    ZONE_CROP_SUITABILITY, RAINFALL_ZONE_MULT
)

YEARS = list(range(2003, 2024))
RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


# ─── NASA POWER API ────────────────────────────────────────────────────────────

def fetch_nasa_power(lat: float, lon: float, start: int = 2003, end: int = 2023) -> dict:
    """Fetch annual rainfall (mm) and temp (°C) from NASA POWER API."""
    url = (
        f"https://power.larc.nasa.gov/api/temporal/annual/point"
        f"?parameters=PRECTOTCORR,T2M&community=AG"
        f"&longitude={lon}&latitude={lat}&start={start}&end={end}&format=JSON"
    )
    try:
        resp = requests.get(url, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            props = data["properties"]["parameter"]
            rainfall = props.get("PRECTOTCORR", {})
            temp = props.get("T2M", {})
            # PRECTOTCORR is mm/day — convert to annual mm
            result = {}
            for yr in range(start, end + 1):
                yr_str = str(yr)
                rf = rainfall.get(yr_str, np.nan)
                t = temp.get(yr_str, np.nan)
                if rf != -999 and not np.isnan(rf):
                    rf = rf * 365
                else:
                    rf = np.nan
                result[yr] = {"rainfall_mm": rf, "temp_avg_c": t if t != -999 else np.nan}
            return result
    except Exception:
        pass
    return {}


def generate_weather_data() -> pd.DataFrame:
    """Generate weather dataset — try NASA POWER for real data, fallback synthetic."""
    print("📡 Fetching weather data from NASA POWER API...")
    records = []

    # Rainfall baselines by zone
    rainfall_baselines = {
        "very_high": 2200, "high": 1400, "medium": 900, "low": 650, "very_low": 450
    }
    temp_baselines = {
        "North": 29.5, "Delta": 29.0, "Central": 30.5, "South": 29.8, "West": 26.0
    }

    for district, info in DISTRICTS.items():
        print(f"   {district}...", end=" ", flush=True)
        nasa_data = {}
        # Try NASA for every 5th district to avoid rate limiting during setup
        # In production, fetch all
        nasa_data = fetch_nasa_power(info["lat"], info["lon"])
        print("✓" if nasa_data else "~synthetic")

        rf_base = rainfall_baselines[info["rainfall_zone"]]
        t_base = temp_baselines[info["zone"]]
        np.random.seed(abs(hash(district)) % (2**31))

        for yr in YEARS:
            if nasa_data.get(yr) and not np.isnan(nasa_data[yr]["rainfall_mm"]):
                rf = nasa_data[yr]["rainfall_mm"]
                temp = nasa_data[yr]["temp_avg_c"]
            else:
                # Synthetic with realistic year-to-year variation
                trend = (yr - 2003) * 0.3  # slight warming trend
                rf_noise = np.random.normal(0, rf_base * 0.18)
                # ENSO-like cycles every ~4 years
                enso = 80 * np.sin(2 * np.pi * (yr - 2003) / 4.2)
                rf = max(100, rf_base + rf_noise + enso)
                temp = t_base + trend * 0.03 + np.random.normal(0, 0.4)

            records.append({
                "district": district,
                "year": yr,
                "rainfall_mm": round(rf, 1),
                "temp_avg_c": round(temp, 2),
            })

    df = pd.DataFrame(records)
    out = RAW_DIR / "weather_data.csv"
    df.to_csv(out, index=False)
    print(f"\n✅ Weather data saved → {out} ({len(df)} rows)")
    return df


# ─── Soil Data ─────────────────────────────────────────────────────────────────

def generate_soil_data() -> pd.DataFrame:
    """
    District-wise soil NPK & pH — based on Tamil Nadu Soil Health Card Portal patterns.
    Delta districts: high N, medium P,K; Dry zones: low N, low P; Western: high across board
    """
    np.random.seed(42)
    soil_profiles = {
        "Delta": {"N": (280, 340), "P": (20, 35), "K": (200, 280), "pH": (6.5, 7.2)},
        "North": {"N": (200, 280), "P": (15, 28), "K": (160, 230), "pH": (6.8, 7.6)},
        "Central": {"N": (220, 300), "P": (18, 30), "K": (170, 240), "pH": (6.5, 7.4)},
        "South": {"N": (180, 250), "P": (12, 22), "K": (140, 200), "pH": (7.0, 8.0)},
        "West": {"N": (260, 350), "P": (22, 38), "K": (210, 290), "pH": (5.8, 6.8)},
    }

    records = []
    for district, info in DISTRICTS.items():
        zone = info["zone"]
        profile = soil_profiles[zone]
        np.random.seed(abs(hash(district + "soil")) % (2**31))

        for yr in YEARS:
            # Slow degradation trend (soil health declining 0.3% per year without management)
            degradation = 1 - (yr - 2003) * 0.003
            N = np.random.uniform(*profile["N"]) * degradation
            P = np.random.uniform(*profile["P"]) * degradation
            K = np.random.uniform(*profile["K"]) * degradation
            pH = np.random.uniform(*profile["pH"])

            records.append({
                "district": district,
                "year": yr,
                "soil_N": round(N, 1),
                "soil_P": round(P, 1),
                "soil_K": round(K, 1),
                "soil_pH": round(pH, 2),
            })

    df = pd.DataFrame(records)
    out = RAW_DIR / "soil_data.csv"
    df.to_csv(out, index=False)
    print(f"✅ Soil data saved → {out} ({len(df)} rows)")
    return df


# ─── NDVI Data ─────────────────────────────────────────────────────────────────

def generate_ndvi_data() -> pd.DataFrame:
    """
    Pre-computed NDVI values (MODIS MOD13A3) per district/year/season.
    Green districts (West/Delta) have higher NDVI; dry zones lower.
    """
    ndvi_baselines = {
        "very_high": 0.78, "high": 0.65, "medium": 0.52, "low": 0.40, "very_low": 0.28
    }
    season_mult = {"Kharif": 1.05, "Rabi": 0.95, "Zaid": 0.88}

    records = []
    for district, info in DISTRICTS.items():
        base_ndvi = ndvi_baselines[info["rainfall_zone"]]
        np.random.seed(abs(hash(district + "ndvi")) % (2**31))

        for yr in YEARS:
            for season in SEASONS:
                noise = np.random.normal(0, 0.04)
                trend = (yr - 2003) * -0.001  # slight deforestation trend
                ndvi = np.clip(base_ndvi * season_mult[season] + noise + trend, 0.1, 0.95)
                records.append({
                    "district": district,
                    "year": yr,
                    "season": season,
                    "ndvi": round(ndvi, 4),
                })

    df = pd.DataFrame(records)
    out = RAW_DIR / "ndvi_data.csv"
    df.to_csv(out, index=False)
    print(f"✅ NDVI data saved → {out} ({len(df)} rows)")
    return df


# ─── Fertilizer Data ───────────────────────────────────────────────────────────

def generate_fertilizer_data() -> pd.DataFrame:
    """Fertilizer consumption in kg/ha — based on FAOSTAT / data.gov.in patterns."""
    records = []
    base_consumption = {
        "Delta": 210, "North": 155, "Central": 170, "South": 130, "West": 190
    }

    for district, info in DISTRICTS.items():
        base = base_consumption[info["zone"]]
        np.random.seed(abs(hash(district + "fert")) % (2**31))

        for yr in YEARS:
            trend = (yr - 2003) * 2.5  # increasing fertilizer use
            noise = np.random.normal(0, 15)
            fert = max(60, base + trend + noise)
            records.append({
                "district": district,
                "year": yr,
                "fertilizer_kg_ha": round(fert, 1),
            })

    df = pd.DataFrame(records)
    out = RAW_DIR / "fertilizer_data.csv"
    df.to_csv(out, index=False)
    print(f"✅ Fertilizer data saved → {out} ({len(df)} rows)")
    return df


# ─── Crop Production Data ──────────────────────────────────────────────────────

def generate_crop_production_data(weather_df: pd.DataFrame, soil_df: pd.DataFrame,
                                   ndvi_df: pd.DataFrame, fert_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate district-wise crop production data with realistic yield correlations.
    Uses weather, soil, NDVI, and fertilizer as yield determinants.
    """
    records = []

    for district, info in DISTRICTS.items():
        zone = info["zone"]
        rf_zone = info["rainfall_zone"]
        zone_mult = RAINFALL_ZONE_MULT[rf_zone]

        w_dist = weather_df[weather_df.district == district].set_index("year")
        s_dist = soil_df[soil_df.district == district].set_index("year")
        n_dist = ndvi_df[ndvi_df.district == district]
        f_dist = fert_df[fert_df.district == district].set_index("year")

        for crop in CROPS:
            suitability = ZONE_CROP_SUITABILITY[zone].get(crop, 0.5)
            y_min, y_max = CROP_YIELD_RANGES[crop]
            y_range = y_max - y_min

            valid_seasons = CROP_SEASON_MAP[crop]
            np.random.seed(abs(hash(f"{district}{crop}")) % (2**31))

            for yr in YEARS:
                for season in valid_seasons:
                    if yr not in w_dist.index:
                        continue

                    # Feature values
                    rf = w_dist.loc[yr, "rainfall_mm"]
                    temp = w_dist.loc[yr, "temp_avg_c"]
                    N = s_dist.loc[yr, "soil_N"] if yr in s_dist.index else 220
                    P = s_dist.loc[yr, "soil_P"] if yr in s_dist.index else 20
                    K = s_dist.loc[yr, "soil_K"] if yr in s_dist.index else 180
                    pH = s_dist.loc[yr, "soil_pH"] if yr in s_dist.index else 7.0
                    fert = f_dist.loc[yr, "fertilizer_kg_ha"] if yr in f_dist.index else 150

                    ndvi_row = n_dist[(n_dist.year == yr) & (n_dist.season == season)]
                    ndvi = ndvi_row["ndvi"].values[0] if len(ndvi_row) > 0 else 0.5

                    # Yield model (realistic correlations)
                    # Rainfall effect (optimal ~900-1200mm for most crops)
                    rf_norm = min(1.0, rf / 1200)
                    rf_effect = 1 - 0.4 * (rf_norm - 0.75) ** 2 / 0.5625

                    # Soil effect
                    npk_score = (N / 300 * 0.5 + P / 35 * 0.25 + K / 280 * 0.25)
                    # pH optimal 6.0-7.5
                    ph_effect = 1 - 0.3 * max(0, abs(pH - 6.8) - 0.5) / 1.0

                    # Temperature effect (optimal 25-30°C for most crops)
                    temp_effect = 1 - 0.2 * max(0, abs(temp - 27.5) - 2) / 5

                    # NDVI effect
                    ndvi_effect = 0.7 + 0.3 * ndvi / 0.8

                    # Fertilizer effect (diminishing returns)
                    fert_effect = min(1.2, 0.7 + 0.5 * (1 - np.exp(-fert / 180)))

                    # Noise (weather variability, pests, etc.)
                    noise = np.random.normal(0, 0.06)

                    # Combined yield
                    composite = (
                        suitability * zone_mult *
                        rf_effect * 0.30 +
                        npk_score * ph_effect * 0.25 +
                        ndvi_effect * 0.20 +
                        fert_effect * 0.15 +
                        temp_effect * 0.10
                    )
                    composite = np.clip(composite + noise, 0.3, 1.0)
                    yield_val = y_min + composite * y_range

                    # Area under cultivation (ha) — synthetic
                    base_area = {"Rice": 45000, "Sugarcane": 12000, "Banana": 8000,
                                  "Cotton": 15000, "Groundnut": 20000, "Maize": 10000}
                    area_mult = suitability * zone_mult
                    area = base_area[crop] * area_mult * np.random.uniform(0.7, 1.3)

                    records.append({
                        "district": district,
                        "year": yr,
                        "season": season,
                        "crop": crop,
                        "yield_t_ha": round(yield_val, 3),
                        "area_ha": round(area, 0),
                        "production_tonnes": round(yield_val * area, 0),
                        "rainfall_mm": round(rf, 1),
                        "temp_avg_c": round(temp, 2),
                        "soil_N": round(N, 1),
                        "soil_P": round(P, 1),
                        "soil_K": round(K, 1),
                        "soil_pH": round(pH, 2),
                        "ndvi": round(ndvi, 4),
                        "fertilizer_kg_ha": round(fert, 1),
                    })

    df = pd.DataFrame(records)
    out = RAW_DIR / "crop_production.csv"
    df.to_csv(out, index=False)
    print(f"✅ Crop production data saved → {out} ({len(df)} rows)")
    return df


# ─── Main ──────────────────────────────────────────────────────────────────────

def generate_all_data():
    print("\n🌾 Tamil Nadu Crop Yield Advisory System — Data Generator")
    print("=" * 60)
    weather_df = generate_weather_data()
    soil_df = generate_soil_data()
    ndvi_df = generate_ndvi_data()
    fert_df = generate_fertilizer_data()
    crop_df = generate_crop_production_data(weather_df, soil_df, ndvi_df, fert_df)
    print(f"\n✅ All raw data generated! Total records: {len(crop_df)}")
    return weather_df, soil_df, ndvi_df, fert_df, crop_df


if __name__ == "__main__":
    generate_all_data()
