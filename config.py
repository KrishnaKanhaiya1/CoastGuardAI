"""
Configuration module - Replace all hardcoded values
Centralized config for easier deployment and maintenance
"""

# ============== GEOGRAPHIC DEFAULTS ==============
DEFAULT_LAT = 10.0
DEFAULT_LON = 76.22
DEFAULT_REGION = "Kochi, Kerala, India"

# ============== EVACUATION PARAMETERS ==============
EVACUATION_SPEED_MS = 1.2  # meters per second (walking speed during evacuation)
EVACUATION_DELAY_MIN = 5   # minutes to realize emergency
SHELTER_CAPACITY_RATIO = 0.8  # 80% of capacity before overflow warning
MAX_EVACUATION_DISTANCE_KM = 10  # Max reasonable evacuation distance

# ============== RISK THRESHOLDS ==============
RISK_LEVEL_CRITICAL = 0.7
RISK_LEVEL_HIGH = 0.4
RISK_LEVEL_MODERATE = 0.2

# ============== CYCLONE PARAMETERS ==============
CYCLONE_CONE_WIDTH_KM = 200
CYCLONE_TRACK_LENGTH = 4
CYCLONE_SPACING_KM = 50

# ============== MANGROVE ASSESSMENT ==============
MANGROVE_WIDTH_STRONG = 100  # meters
MANGROVE_WIDTH_GOOD = 70
MANGROVE_WIDTH_FAIR = 50
MANGROVE_WIDTH_WEAK = 30

# ============== LIVE DATA ==============
LIVE_FEED_TIMEOUT_SEC = 10
LIVE_FEED_CACHE_MIN = 5  # Cache live data for 5 minutes

# ============== API CONFIGURATION ==============
API_HOST = "0.0.0.0"
API_PORT = 5000
API_VERSION = "1.0"
API_DEBUG = False

# ============== SUPPORTED LANGUAGES ==============
SUPPORTED_LANGUAGES = ["English", "Malayalam", "Tamil"]
DEFAULT_LANGUAGE = "English"

# ============== FILE PATHS ==============
DATA_SHELTERS_FILE = "data_shelters.json"
DATA_REPORTS_FILE = "data_reports.json"

# ============== FEATURE FLAGS ==============
ENABLE_LIVE_WEATHER = True
ENABLE_CYCLONE_SIM = True
ENABLE_VESSEL_TRACKING = True
ENABLE_BLUE_ECONOMY = True

# ============== VALIDATION CONSTRAINTS ==============
LAT_MIN = 8.0      # Southern limit for Kerala
LAT_MAX = 12.5     # Northern limit for Kerala
LON_MIN = 74.0     # Western limit (Arabian Sea)
LON_MAX = 78.0     # Eastern limit for India
