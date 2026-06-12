"""
Setup script to run the entire data pipeline and train models from scratch.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from utils.data_generator import generate_all_data
from utils.feature_engineer import engineer_features
from utils.model_trainer import train_models

def main():
    print("🚀 Starting TN Crop Yield Advisory System Setup...")
    
    # Step 1: Generate Data
    weather_df, soil_df, ndvi_df, fert_df, crop_df = generate_all_data()
    
    # Step 2: Engineer Features
    engineered_df = engineer_features(crop_df)
    
    # Step 3: Train Models
    train_models()
    
    print("\n🎉 Setup Complete! You can now run the Streamlit app:")
    print("streamlit run app/main.py")

if __name__ == "__main__":
    main()
