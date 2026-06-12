"""
Feature engineering module. Adds rolling averages, lag features, and composite scores.
"""
import pandas as pd
from pathlib import Path

PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def engineer_features(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply feature engineering to the raw dataset.
    - rainfall_3yr_avg: 3-year moving average of rainfall.
    - yield_lag1: Last year's yield for the same district and crop.
    - soil_fertility_score: Combined metric of N, P, K, pH.
    """
    print("🔧 Engineering features...")
    df = raw_df.copy()
    
    # Sort for rolling calculations
    df = df.sort_values(by=["district", "crop", "season", "year"])
    
    # 1. 3-Year Rainfall Moving Average
    # Group by district, season, year (assuming 1 record per district/season/year or we take mean first)
    # Since we have rainfall at the row level which is annual, we can just group by district and year first to get unique district-year rainfall
    rainfall_yearly = df.groupby(['district', 'year'])['rainfall_mm'].mean().reset_index()
    rainfall_yearly = rainfall_yearly.sort_values(by=['district', 'year'])
    rainfall_yearly['rainfall_3yr_avg'] = rainfall_yearly.groupby('district')['rainfall_mm'].transform(lambda x: x.rolling(window=3, min_periods=1).mean())
    
    df = df.merge(rainfall_yearly[['district', 'year', 'rainfall_3yr_avg']], on=['district', 'year'], how='left')

    # 2. Lag Feature: Last Year Yield (yield_lag1)
    df['yield_lag1'] = df.groupby(['district', 'crop', 'season'])['yield_t_ha'].shift(1)
    # Fill NaN for first year with district-crop mean
    mean_yields = df.groupby(['district', 'crop'])['yield_t_ha'].transform('mean')
    df['yield_lag1'] = df['yield_lag1'].fillna(mean_yields)

    # 3. Combined Soil Fertility Score
    # Normalize N, P, K based on standard optimal values (N: 300, P: 35, K: 280)
    # pH score: 1.0 at 6.8, decays as it moves away
    df['n_norm'] = df['soil_N'] / 300
    df['p_norm'] = df['soil_P'] / 35
    df['k_norm'] = df['soil_K'] / 280
    df['ph_score'] = 1 - 0.3 * abs(df['soil_pH'] - 6.8)
    df['ph_score'] = df['ph_score'].clip(lower=0.1)
    
    df['soil_fertility_score'] = (df['n_norm'] * 0.4 + df['p_norm'] * 0.3 + df['k_norm'] * 0.3) * df['ph_score']
    df['soil_fertility_score'] = df['soil_fertility_score'].round(3)
    
    # Cleanup intermediate columns
    df = df.drop(columns=['n_norm', 'p_norm', 'k_norm', 'ph_score'])

    out = PROCESSED_DIR / "engineered_data.csv"
    df.to_csv(out, index=False)
    print(f"✅ Feature engineering complete! Saved → {out} ({len(df)} rows)")
    return df

if __name__ == "__main__":
    RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
    raw_path = RAW_DIR / "crop_production.csv"
    if raw_path.exists():
        raw_df = pd.read_csv(raw_path)
        engineer_features(raw_df)
    else:
        print("❌ Raw data not found. Please run data_generator.py first.")
