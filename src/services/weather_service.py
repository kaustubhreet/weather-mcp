"""
Business logic for weather-related operations.
"""

from typing import Optional

from src.clients.weather_client import WeatherClient
from src.logger import logger
from src.models.weather_model import (
    Coordinates,
    CurrentWeather,
    ForecastEntry,
    Temperature,
    WeatherCondition,
    WeatherForecast,
    Wind,
)
from src.config import DEFAULT_UNITS


class WeatherService:
    """Orchestrates fetching and transforming weather data."""

    def __init__(self, client: Optional[WeatherClient] = None) -> None:
        self._client = client or WeatherClient()
        logger.info("WeatherService initialised")

    async def close(self) -> None:
        await self._client.close()

    # ── Helpers ────────────────────────────────────────────────────

    @staticmethod
    def _to_temperature(d: dict) -> Temperature:
        return Temperature(
            temp=d["temp"],
            feels_like=d["feels_like"],
            temp_min=d["temp_min"],
            temp_max=d["temp_max"],
            humidity=d["humidity"],
            pressure=d["pressure"],
        )

    @staticmethod
    def _to_condition(d: dict) -> WeatherCondition:
        return WeatherCondition(
            id=d["id"],
            main=d["main"],
            description=d["description"],
            icon=d["icon"],
        )

    @staticmethod
    def _to_wind(d: dict) -> Wind:
        return Wind(
            speed=d["speed"],
            deg=d["deg"],
            gust=d.get("gust"),
        )

    async def _resolve_coordinates(
        self, city: Optional[str] = None, lat: Optional[float] = None, lon: Optional[float] = None
    ) -> tuple[float, float, str, str]:
        """Return (lat, lon, city_name, country_code)."""
        if city:
            results = await self._client.geocode(city)
            hit = results[0]
            return hit["lat"], hit["lon"], hit.get("name", city), hit.get("country", "")
        if lat is not None and lon is not None:
            # try reverse geocode for a human-friendly name
            try:
                results = await self._client.reverse_geocode(lat, lon)
                rev = results[0]
                city_name = rev.get("name", f"{lat},{lon}")
                country = rev.get("country", "")
                return lat, lon, city_name, country
            except Exception:
                return lat, lon, f"{lat},{lon}", ""
        raise ValueError("Provide either a city name or (lat, lon) coordinates.")

    # ── Current weather ────────────────────────────────────────────

    async def get_current_weather(
        self,
        city: Optional[str] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        units: str = DEFAULT_UNITS,
    ) -> CurrentWeather:
        """Get current weather for a city or coordinates."""
        lat_r, lon_r, city_name, country = await self._resolve_coordinates(city, lat, lon)
        raw = await self._client.current_weather(lat_r, lon_r, units)
        return self._parse_current(raw, city_name, country)

    def _parse_current(self, raw: dict, city_name: str, country: str) -> CurrentWeather:
        return CurrentWeather(
            city=city_name,
            country=country,
            coordinates=Coordinates(lat=raw["coord"]["lat"], lon=raw["coord"]["lon"]),
            condition=self._to_condition(raw["weather"][0]),
            temperature=self._to_temperature(raw["main"]),
            wind=self._to_wind(raw["wind"]),
            visibility=raw.get("visibility", 0),
            clouds=raw.get("clouds", {}).get("all", 0),
            dt=raw["dt"],
            timezone=raw.get("timezone", 0),
        )

    # ── Forecast ───────────────────────────────────────────────────

    async def get_forecast(
        self,
        city: Optional[str] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        units: str = DEFAULT_UNITS,
        periods: int = 8,
    ) -> WeatherForecast:
        """Get weather forecast for a city or coordinates."""
        lat_r, lon_r, city_name, country = await self._resolve_coordinates(city, lat, lon)
        raw = await self._client.forecast(lat_r, lon_r, units, cnt=periods)
        return self._parse_forecast(raw, city_name, country)

    def _parse_forecast(self, raw: dict, city_name: str, country: str) -> WeatherForecast:
        entries: list[ForecastEntry] = []
        for item in raw.get("list", []):
            entries.append(
                ForecastEntry(
                    dt=item["dt"],
                    temperature=self._to_temperature(item["main"]),
                    wind=self._to_wind(item["wind"]),
                    condition=self._to_condition(item["weather"][0]),
                    clouds=item.get("clouds", {}).get("all", 0),
                    pop=item.get("pop", 0.0),
                )
            )
        return WeatherForecast(city=city_name, country=country, entries=entries)

