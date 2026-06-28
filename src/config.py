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
