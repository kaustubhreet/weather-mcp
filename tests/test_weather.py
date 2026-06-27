"""
Unit tests for weather-mcp components.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from src.clients.weather_client import WeatherClient, WeatherClientError
from src.models.weather_model import (
    CurrentWeather,
    ForecastEntry,
    Temperature,
    WeatherCondition,
    WeatherForecast,
    Wind,
)
from src.services.weather_service import WeatherService
from src.tools.weather import CURRENT_WEATHER_TOOL, FORECAST_TOOL


# ═══════════════════════════════════════════════════════════════════
#  Models
# ═══════════════════════════════════════════════════════════════════

class TestCurrentWeather:
    def test_summary(self):
        t = Temperature(temp=22.5, feels_like=20.0, temp_min=18.0,
                         temp_max=25.0, humidity=60, pressure=1013)
        w = Wind(speed=3.5, deg=180)
        c = WeatherCondition(id=800, main="Clear", description="clear sky",
                             icon="01d")
        cw = CurrentWeather(
            city="London", country="GB", condition=c, temperature=t,
            wind=w, visibility=10000, clouds=0, dt=1700000000, timezone=0,
            coordinates=MagicMock(),
        )
        assert "London" in cw.summary
        assert "22.5°C" in cw.summary
        assert cw.temp_celsius == 22.5


class TestWeatherForecast:
    def test_summary(self):
        wf = WeatherForecast(city="Paris", country="FR", entries=[])
        assert "Paris" in wf.summary
        assert "0 forecast" in wf.summary


# ═══════════════════════════════════════════════════════════════════
#  Client
# ═══════════════════════════════════════════════════════════════════

class TestWeatherClient:
    @patch("src.clients.weather_client.WEATHER_API_KEY", "")
    def test_missing_api_key(self):
        with pytest.raises(WeatherClientError, match="WEATHER_API_KEY"):
            WeatherClient()

    @pytest.mark.asyncio
    @patch("src.clients.weather_client.WEATHER_API_KEY", "test-key")
    @patch("src.clients.weather_client.httpx.AsyncClient")
    async def test_geocode_success(self, mock_client_cls):
        mock_resp = MagicMock()
        mock_resp.json.return_value = [{"lat": 51.5, "lon": -0.12,
                                        "name": "London", "country": "GB"}]
        mock_instance = MagicMock()
        mock_instance.get = AsyncMock(return_value=mock_resp)
        mock_client_cls.return_value = mock_instance

        client = WeatherClient()
        result = await client.geocode("London")
        assert result[0]["lat"] == 51.5

    @pytest.mark.asyncio
    @patch("src.clients.weather_client.WEATHER_API_KEY", "test-key")
    @patch("src.clients.weather_client.httpx.AsyncClient")
    async def test_geocode_not_found(self, mock_client_cls):
        mock_resp = MagicMock()
        mock_resp.json.return_value = []
        mock_instance = MagicMock()
        mock_instance.get = AsyncMock(return_value=mock_resp)
        mock_client_cls.return_value = mock_instance

        client = WeatherClient()
        with pytest.raises(WeatherClientError, match="not found"):
            await client.geocode("Nowhereville")


# ═══════════════════════════════════════════════════════════════════
#  Service
# ═══════════════════════════════════════════════════════════════════

class TestWeatherService:
    @pytest.fixture
    def mock_client(self):
        client = MagicMock(spec=WeatherClient)
        client.geocode = AsyncMock(return_value=[
            {"lat": 48.8566, "lon": 2.3522, "name": "Paris", "country": "FR"},
        ])
        client.current_weather = AsyncMock(return_value={
            "coord": {"lat": 48.86, "lon": 2.35},
            "weather": [{"id": 800, "main": "Clear",
                         "description": "clear sky", "icon": "01d"}],
            "main": {"temp": 25.0, "feels_like": 24.0,
                     "temp_min": 22.0, "temp_max": 28.0,
                     "humidity": 50, "pressure": 1015},
            "wind": {"speed": 4.1, "deg": 200, "gust": 6.0},
            "visibility": 10000,
            "clouds": {"all": 10},
            "dt": 1700000000,
            "timezone": 3600,
        })
        client.forecast = AsyncMock(return_value={
            "list": [
                {
                    "dt": 1700000000,
                    "main": {"temp": 24.0, "feels_like": 23.0,
                             "temp_min": 22.0, "temp_max": 26.0,
                             "humidity": 55, "pressure": 1014},
                    "wind": {"speed": 3.0, "deg": 180},
                    "weather": [{"id": 801, "main": "Clouds",
                                 "description": "few clouds", "icon": "02d"}],
                    "clouds": {"all": 20},
                    "pop": 0.1,
                }
            ]
        })
        return client

    @pytest.mark.asyncio
    async def test_get_current_weather(self, mock_client):
        service = WeatherService(client=mock_client)
        result = await service.get_current_weather(city="Paris")
        assert isinstance(result, CurrentWeather)
        assert result.city == "Paris"
        assert result.temperature.temp == 25.0
        assert result.condition.main == "Clear"

    @pytest.mark.asyncio
    async def test_get_forecast(self, mock_client):
        service = WeatherService(client=mock_client)
        result = await service.get_forecast(city="Paris", periods=1)
        assert isinstance(result, WeatherForecast)
        assert len(result.entries) == 1
        assert result.entries[0].pop == 0.1


# ═══════════════════════════════════════════════════════════════════
#  Tool schemas
# ═══════════════════════════════════════════════════════════════════

class TestToolSchemas:
    def test_current_weather_schema(self):
        assert CURRENT_WEATHER_TOOL.name == "get_current_weather"
        props = CURRENT_WEATHER_TOOL.inputSchema["properties"]
        assert "city" in props
        assert "lat" in props

    def test_forecast_schema(self):
        assert FORECAST_TOOL.name == "get_forecast"
        props = FORECAST_TOOL.inputSchema["properties"]
        assert "periods" in props
        assert props["periods"]["maximum"] == 40


# ═══════════════════════════════════════════════════════════════════
#  Helper
# ═══════════════════════════════════════════════════════════════════

def asyncio_run(coro):
    """Run a coroutine synchronously (for tests)."""
    import asyncio
    return asyncio.run(coro)

