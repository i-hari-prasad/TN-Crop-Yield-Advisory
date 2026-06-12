"""
Model training module. Trains Linear Regression, Random Forest, XGBoost, and LSTM models.
"""
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from xgboost import XGBRegressor
import warnings
warnings.filterwarnings('ignore')

try:
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.callbacks import EarlyStopping
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    print("Warning: TensorFlow not found. LSTM model will not be trained.")

MODELS_DIR = Path(__file__).parent.parent / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"

# Features to use for prediction
FEATURES = [
    'rainfall_mm', 'rainfall_3yr_avg', 'temp_avg_c',
    'soil_N', 'soil_P', 'soil_K', 'soil_pH', 'soil_fertility_score',
    'ndvi', 'fertilizer_kg_ha', 'yield_lag1',
    'district_encoded', 'crop_encoded', 'season_encoded'
]
TARGET = 'yield_t_ha'

def evaluate_model(name, y_true, y_pred):
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    print(f"--- {name} ---")
    print(f"R² Score: {r2:.4f}")
    print(f"RMSE:     {rmse:.4f} t/ha")
    print(f"MAE:      {mae:.4f} t/ha")
    return r2, rmse, mae

def train_models():
    data_path = PROCESSED_DIR / "engineered_data.csv"
    if not data_path.exists():
        print("❌ Engineered data not found.")
        return
        
    print("🧠 Starting Model Training Phase...")
    df = pd.read_csv(data_path)
    
    # Label Encoding for categorical variables
    le_district = LabelEncoder()
    le_crop = LabelEncoder()
    le_season = LabelEncoder()
    
    df['district_encoded'] = le_district.fit_transform(df['district'])
    df['crop_encoded'] = le_crop.fit_transform(df['crop'])
    df['season_encoded'] = le_season.fit_transform(df['season'])
    
    # Save encoders
    joblib.dump(le_district, MODELS_DIR / 'le_district.pkl')
    joblib.dump(le_crop, MODELS_DIR / 'le_crop.pkl')
    joblib.dump(le_season, MODELS_DIR / 'le_season.pkl')
    
    # Train-test split (chronological or random. Using random here for overall metric, 
    # but LSTM will use chronological)
    X = df[FEATURES]
    y = df[TARGET]
    
    # Save feature names for SHAP
    joblib.dump(FEATURES, MODELS_DIR / 'feature_names.pkl')
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    joblib.dump(scaler, MODELS_DIR / 'scaler.pkl')
    
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    
    # 1. Linear Regression
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)
    evaluate_model("Linear Regression", y_test, y_pred_lr)
    joblib.dump(lr, MODELS_DIR / 'linear_regression.pkl')
    
    # 2. Random Forest
    rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    evaluate_model("Random Forest", y_test, y_pred_rf)
    joblib.dump(rf, MODELS_DIR / 'random_forest.pkl')
    
    # 3. XGBoost (Primary)
    xgb = XGBRegressor(n_estimators=200, learning_rate=0.05, max_depth=6, random_state=42, n_jobs=-1)
    xgb.fit(X_train, y_train)
    y_pred_xgb = xgb.predict(X_test)
    r2_xgb, rmse_xgb, mae_xgb = evaluate_model("XGBoost", y_test, y_pred_xgb)
    joblib.dump(xgb, MODELS_DIR / 'xgboost_model.pkl')
    
    if r2_xgb >= 0.82 and rmse_xgb <= 0.4 and mae_xgb <= 0.3:
        print("✅ XGBoost meets target performance criteria!")
    else:
        print("⚠️ XGBoost did not meet all target performance criteria.")

    # 4. LSTM (Time-series trend forecasting per district-crop)
    if TF_AVAILABLE:
        print("\n⏳ Training LSTM...")
        # Prepare sequence data
        # We'll build a simplified LSTM that takes the last 3 years of features to predict next year
        seq_length = 3
        lstm_X, lstm_y = [], []
        
        # We need data sorted by time for each group
        df_sorted = df.sort_values(by=['district', 'crop', 'season', 'year'])
        grouped = df_sorted.groupby(['district', 'crop', 'season'])
        
        for name, group in grouped:
            # Only use if enough history
            if len(group) > seq_length:
                group_features = scaler.transform(group[FEATURES])
                group_targets = group[TARGET].values
                
                for i in range(len(group_features) - seq_length):
                    lstm_X.append(group_features[i:i+seq_length])
                    lstm_y.append(group_targets[i+seq_length])
                    
        lstm_X = np.array(lstm_X)
        lstm_y = np.array(lstm_y)
        
        if len(lstm_X) > 0:
            X_train_l, X_test_l, y_train_l, y_test_l = train_test_split(lstm_X, lstm_y, test_size=0.2, random_state=42)
            
            model = Sequential()
            model.add(LSTM(64, activation='relu', input_shape=(seq_length, len(FEATURES)), return_sequences=False))
            model.add(Dropout(0.2))
            model.add(Dense(32, activation='relu'))
            model.add(Dense(1))
            
            model.compile(optimizer='adam', loss='mse')
            early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
            
            model.fit(X_train_l, y_train_l, epochs=50, batch_size=32, validation_split=0.2, callbacks=[early_stop], verbose=0)
            
            y_pred_l = model.predict(X_test_l, verbose=0).flatten()
            evaluate_model("LSTM", y_test_l, y_pred_l)
            model.save(MODELS_DIR / 'lstm_model.h5')
            print("✅ LSTM trained and saved.")
        else:
            print("⚠️ Not enough sequence data for LSTM.")

    print("\n✅ All models trained successfully!")

if __name__ == "__main__":
    train_models()
