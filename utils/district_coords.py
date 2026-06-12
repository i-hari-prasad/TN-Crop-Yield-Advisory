"""
Tamil Nadu District Coordinates & Metadata
All 38 districts with headquarters lat/long for NASA POWER & OWM API calls.
"""

DISTRICTS = {
    "Ariyalur": {"lat": 11.1404, "lon": 79.0755, "zone": "North", "rainfall_zone": "medium"},
    "Chengalpattu": {"lat": 12.6921, "lon": 79.9898, "zone": "North", "rainfall_zone": "medium"},
    "Chennai": {"lat": 13.0827, "lon": 80.2707, "zone": "North", "rainfall_zone": "medium"},
    "Coimbatore": {"lat": 11.0168, "lon": 76.9558, "zone": "West", "rainfall_zone": "high"},
    "Cuddalore": {"lat": 11.7447, "lon": 79.7689, "zone": "North", "rainfall_zone": "high"},
    "Dharmapuri": {"lat": 12.1211, "lon": 78.1582, "zone": "North", "rainfall_zone": "low"},
    "Dindigul": {"lat": 10.3673, "lon": 77.9803, "zone": "South", "rainfall_zone": "medium"},
    "Erode": {"lat": 11.3410, "lon": 77.7172, "zone": "West", "rainfall_zone": "medium"},
    "Kallakurichi": {"lat": 11.7380, "lon": 78.9592, "zone": "North", "rainfall_zone": "medium"},
    "Kancheepuram": {"lat": 12.8185, "lon": 79.6947, "zone": "North", "rainfall_zone": "medium"},
    "Kanyakumari": {"lat": 8.0883, "lon": 77.5385, "zone": "South", "rainfall_zone": "high"},
    "Karur": {"lat": 10.9601, "lon": 78.0766, "zone": "Central", "rainfall_zone": "medium"},
    "Krishnagiri": {"lat": 12.5186, "lon": 78.2136, "zone": "North", "rainfall_zone": "low"},
    "Madurai": {"lat": 9.9252, "lon": 78.1198, "zone": "South", "rainfall_zone": "low"},
    "Mayiladuthurai": {"lat": 11.1015, "lon": 79.6542, "zone": "Delta", "rainfall_zone": "high"},
    "Nagapattinam": {"lat": 10.7672, "lon": 79.8449, "zone": "Delta", "rainfall_zone": "high"},
    "Namakkal": {"lat": 11.2189, "lon": 78.1676, "zone": "Central", "rainfall_zone": "medium"},
    "Nilgiris": {"lat": 11.4916, "lon": 76.7337, "zone": "West", "rainfall_zone": "very_high"},
    "Perambalur": {"lat": 11.2333, "lon": 78.8834, "zone": "Central", "rainfall_zone": "low"},
    "Pudukkottai": {"lat": 10.3797, "lon": 78.8236, "zone": "South", "rainfall_zone": "low"},
    "Ramanathapuram": {"lat": 9.3639, "lon": 78.8395, "zone": "South", "rainfall_zone": "very_low"},
    "Ranipet": {"lat": 12.9224, "lon": 79.3328, "zone": "North", "rainfall_zone": "medium"},
    "Salem": {"lat": 11.6643, "lon": 78.1460, "zone": "Central", "rainfall_zone": "medium"},
    "Sivaganga": {"lat": 9.8477, "lon": 78.4800, "zone": "South", "rainfall_zone": "low"},
    "Tenkasi": {"lat": 8.9592, "lon": 77.3152, "zone": "South", "rainfall_zone": "high"},
    "Thanjavur": {"lat": 10.7870, "lon": 79.1378, "zone": "Delta", "rainfall_zone": "high"},
    "Theni": {"lat": 10.0104, "lon": 77.4770, "zone": "South", "rainfall_zone": "high"},
    "Thoothukudi": {"lat": 8.7642, "lon": 78.1348, "zone": "South", "rainfall_zone": "very_low"},
    "Tiruchirappalli": {"lat": 10.7905, "lon": 78.7047, "zone": "Central", "rainfall_zone": "medium"},
    "Tirunelveli": {"lat": 8.7139, "lon": 77.7567, "zone": "South", "rainfall_zone": "medium"},
    "Tirupathur": {"lat": 12.4960, "lon": 78.5707, "zone": "North", "rainfall_zone": "low"},
    "Tiruppur": {"lat": 11.1085, "lon": 77.3411, "zone": "West", "rainfall_zone": "medium"},
    "Tiruvallur": {"lat": 13.1435, "lon": 79.9080, "zone": "North", "rainfall_zone": "medium"},
    "Tiruvannamalai": {"lat": 12.2306, "lon": 79.0748, "zone": "North", "rainfall_zone": "medium"},
    "Tiruvarur": {"lat": 10.7659, "lon": 79.6340, "zone": "Delta", "rainfall_zone": "high"},
    "Vellore": {"lat": 12.9165, "lon": 79.1325, "zone": "North", "rainfall_zone": "medium"},
    "Villupuram": {"lat": 11.9402, "lon": 79.4861, "zone": "North", "rainfall_zone": "medium"},
    "Virudhunagar": {"lat": 9.5880, "lon": 77.9624, "zone": "South", "rainfall_zone": "low"},
}

DISTRICT_NAMES = sorted(DISTRICTS.keys())

# Crop-specific characteristics per district zone
ZONE_CROP_SUITABILITY = {
    "Delta": {
        "Rice": 1.0, "Sugarcane": 0.9, "Banana": 0.8,
        "Cotton": 0.3, "Groundnut": 0.4, "Maize": 0.6
    },
    "North": {
        "Rice": 0.7, "Sugarcane": 0.6, "Banana": 0.6,
        "Cotton": 0.7, "Groundnut": 0.6, "Maize": 0.7
    },
    "South": {
        "Rice": 0.6, "Sugarcane": 0.5, "Banana": 0.7,
        "Cotton": 0.7, "Groundnut": 0.8, "Maize": 0.6
    },
    "Central": {
        "Rice": 0.65, "Sugarcane": 0.75, "Banana": 0.7,
        "Cotton": 0.6, "Groundnut": 0.7, "Maize": 0.75
    },
    "West": {
        "Rice": 0.7, "Sugarcane": 0.85, "Banana": 0.9,
        "Cotton": 0.5, "Groundnut": 0.5, "Maize": 0.65
    },
}

# Baseline yield ranges (t/ha) per crop
CROP_YIELD_RANGES = {
    "Rice": (1.5, 4.5),
    "Sugarcane": (50.0, 110.0),
    "Banana": (15.0, 42.0),
    "Cotton": (0.3, 1.6),
    "Groundnut": (0.5, 2.8),
    "Maize": (1.5, 5.0),
}

CROPS = list(CROP_YIELD_RANGES.keys())
SEASONS = ["Kharif", "Rabi", "Zaid"]

# Crop-season validity (not all crops grow in all seasons)
CROP_SEASON_MAP = {
    "Rice": ["Kharif", "Rabi"],
    "Sugarcane": ["Kharif"],
    "Banana": ["Kharif", "Rabi", "Zaid"],
    "Cotton": ["Kharif"],
    "Groundnut": ["Kharif", "Rabi", "Zaid"],
    "Maize": ["Kharif", "Rabi", "Zaid"],
}

# Rainfall zone multipliers
RAINFALL_ZONE_MULT = {
    "very_high": 1.25,
    "high": 1.10,
    "medium": 1.00,
    "low": 0.85,
    "very_low": 0.70,
}
