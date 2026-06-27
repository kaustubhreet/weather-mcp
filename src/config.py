"""
Application configuration — loads environment variables and provides constants.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── OpenWeatherMap ────────────────────────────────────────────────
WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY", "")
WEATHER_BASE_URL: str = os.getenv(
    "WEATHER_BASE_URL",
    "https://api.openweathermap.org/data/2.5",
)
WEATHER_GEO_URL: str = "https://api.openweathermap.org/geo/1.0"

# ── Units ─────────────────────────────────────────────────────────
DEFAULT_UNITS: str = "metric"  # "metric", "imperial", or "standard"

# ── Server ────────────────────────────────────────────────────────
MCP_SERVER_NAME: str = "weather-mcp"
MCP_SERVER_VERSION: str = "1.0.0"

BASE_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

CITIES = {
    "delhi": (28.6139, 77.2090),
    "mumbai": (19.0760, 72.8777),
    "bangalore": (12.9716, 77.5946),
    "kolkata": (22.5726, 88.3639),
}