"""
Open-Meteo API integration for live weather data.
"""
import requests

# Default fallback values for TN if API fails
FALLBACK_WEATHER = {
    "temp_c": 30.5,
    "rainfall_mm": 2.5
}

def get_live_weather(lat: float, lon: float, api_key: str = None) -> dict:
    """
    Fetch current temperature and daily precipitation from Open-Meteo.
    This API is completely free and requires NO API key!
    """
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,precipitation&timezone=Asia/Kolkata"
    
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            current = data.get("current", {})
            
            temp = current.get("temperature_2m", FALLBACK_WEATHER["temp_c"])
            rain = current.get("precipitation", 0.0)
            
            return {
                "temp_c": temp,
                "rainfall_mm": rain
            }
    except Exception:
        pass
        
    return FALLBACK_WEATHER
