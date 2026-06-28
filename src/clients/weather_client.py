"""
HTTP client for the OpenWeatherMap API.
"""

from typing import Optional

import httpx

from src.config import WEATHER_API_KEY, WEATHER_BASE_URL, WEATHER_GEO_URL
from src.logger import logger


class WeatherClientError(Exception):
    """Raised when the upstream API returns an error."""


class WeatherClient:
    """Thin wrapper around OpenWeatherMap endpoints."""

    def __init__(self, api_key: Optional[str] = None) -> None:
        self._api_key = api_key or WEATHER_API_KEY
        if not self._api_key:
            raise WeatherClientError(
                "WEATHER_API_KEY is not set. "
                "Provide a key or set the WEATHER_API_KEY environment variable."
            )
        self._client = httpx.AsyncClient(timeout=httpx.Timeout(10.0))
        logger.info("WeatherClient initialised")

    async def close(self) -> None:
        await self._client.aclose()

    # ── Private helpers ─────────────────────────────────────────────

    async def _get(self, url: str, params: dict) -> dict:
        """Perform a GET request and return the decoded JSON body."""
        logger.debug("GET %s  params=%s", url, params)
        resp = await self._client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    # ── Geocoding ──────────────────────────────────────────────────

    async def geocode(self, city: str, limit: int = 5) -> list[dict]:
        """Look up coordinates for a city name."""
        data = await self._get(
            f"{WEATHER_GEO_URL}/direct",
            {"q": city, "limit": limit, "appid": self._api_key},
        )
        if not data:
            raise WeatherClientError(f"City {city!r} not found.")
        return data

    async def reverse_geocode(self, lat: float, lon: float) -> list[dict]:
        """Look up location name from coordinates."""
        data = await self._get(
            f"{WEATHER_GEO_URL}/reverse",
            {"lat": lat, "lon": lon, "limit": 1, "appid": self._api_key},
        )
        if not data:
            raise WeatherClientError(f"No location found for ({lat}, {lon}).")
        return data

    # ── Current weather ────────────────────────────────────────────

    async def current_weather(
        self, lat: float, lon: float, units: str = "metric"
    ) -> dict:
        """Fetch current weather for the given coordinates."""
        return await self._get(
            f"{WEATHER_BASE_URL}/weather",
            {"lat": lat, "lon": lon, "appid": self._api_key, "units": units},
        )

    # ── 5‑day / 3‑hour forecast ────────────────────────────────────

    async def forecast(
        self, lat: float, lon: float, units: str = "metric", cnt: int = 8
    ) -> dict:
        """Fetch forecast data (default 8 periods = 24 h worth of 3-hourly)."""
        return await self._get(
            f"{WEATHER_BASE_URL}/forecast",
            {"lat": lat, "lon": lon, "appid": self._api_key, "units": units, "cnt": cnt},
        )
