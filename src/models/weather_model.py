"""
Data models for weather information.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Coordinates:
    """Geographic coordinates."""

    lat: float
    lon: float


@dataclass
class WeatherCondition:
    """Short description of current weather."""

    id: int
    main: str
    description: str
    icon: str


@dataclass
class Temperature:
    """Temperature data."""

    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    humidity: int
    pressure: int


@dataclass
class Wind:
    """Wind data."""

    speed: float
    deg: int
    gust: Optional[float] = None


@dataclass
class CurrentWeather:
    """Complete current weather for a location."""

    city: str
    country: str
    coordinates: Coordinates
    condition: WeatherCondition
    temperature: Temperature
    wind: Wind
    visibility: int
    clouds: int
    dt: int
    timezone: int

    @property
    def temp_celsius(self) -> float:
        return self.temperature.temp

    @property
    def summary(self) -> str:
        """Human-readable one-line summary."""
        t = self.temperature
        return (
            f"{self.city}, {self.country}: {self.condition.description}, "
            f"{t.temp:.1f}°C (feels like {t.feels_like:.1f}°C), "
            f"humidity {t.humidity}%, wind {self.wind.speed:.1f} m/s"
        )


@dataclass
class ForecastEntry:
    """Single forecast data point (3-hour or daily)."""

    dt: int
    temperature: Temperature
    wind: Wind
    condition: WeatherCondition
    clouds: int
    pop: float  # Probability of precipitation


@dataclass
class WeatherForecast:
    """Multi-day or multi-period forecast."""

    city: str
    country: str
    entries: list[ForecastEntry] = field(default_factory=list)

    @property
    def summary(self) -> str:
        return f"{self.city}, {self.country}: {len(self.entries)} forecast periods"

