"""
MCP tool definitions for weather operations.
"""

from typing import Optional

from mcp.server import Server
from mcp.types import Tool, TextContent

from src.logger import logger
from src.services.weather_service import WeatherService
from src.utils.helpers import timestamp_to_str

# ── Tool schemas (JSON Schema for each tool) ──────────────────────

CURRENT_WEATHER_TOOL = Tool(
    name="get_current_weather",
    description="Get the current weather for a city or GPS coordinates.",
    inputSchema={
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "City name (e.g. 'London,GB' or 'Tokyo')",
            },
            "lat": {"type": "number", "description": "Latitude (-90 to 90)"},
            "lon": {"type": "number", "description": "Longitude (-180 to 180)"},
            "units": {
                "type": "string",
                "enum": ["metric", "imperial", "standard"],
                "description": "Units of measurement (default: metric)",
            },
        },
        "anyOf": [
            {"required": ["city"]},
            {"required": ["lat", "lon"]},
        ],
        "additionalProperties": False,
    },
)

FORECAST_TOOL = Tool(
    name="get_forecast",
    description="Get a weather forecast (3‑hourly periods) for a city or coordinates.",
    inputSchema={
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City name"},
            "lat": {"type": "number", "description": "Latitude"},
            "lon": {"type": "number", "description": "Longitude"},
            "units": {
                "type": "string",
                "enum": ["metric", "imperial", "standard"],
                "description": "Units of measurement (default: metric)",
            },
            "periods": {
                "type": "integer",
                "description": "Number of 3‑hour periods to return (default 8 = 24 h)",
                "minimum": 1,
                "maximum": 40,
            },
        },
        "anyOf": [
            {"required": ["city"]},
            {"required": ["lat", "lon"]},
        ],
        "additionalProperties": False,
    },
)

# ── Tool handler ──────────────────────────────────────────────────


def register_tools(server: Server, service: WeatherService) -> None:
    """Register all tools with the MCP server instance."""

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [CURRENT_WEATHER_TOOL, FORECAST_TOOL]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict | None,) -> list[TextContent]:
        logger.info("Tool called: %s %s", name, arguments)
        arguments = arguments or {}
        
        if name == "get_current_weather":
            return [await _handle_current_weather(service, arguments)]
        elif name == "get_forecast":
            return [await _handle_forecast(service, arguments)]
        else:
            raise ValueError(f"Unknown tool: {name}")


# ── Individual handlers ───────────────────────────────────────────


async def _handle_current_weather(
    service: WeatherService, args: dict
) -> TextContent:
    city = args.get("city")
    lat = args.get("lat")
    lon = args.get("lon")
    units = args.get("units", "metric")

    weather = await service.get_current_weather(
        city=city, lat=lat, lon=lon, units=units
    )

    lines = [
        f"🌤  **{weather.city}, {weather.country}**",
        f"   {weather.condition.description.capitalize()}  "
        f"({weather.condition.main})",
        f"   Temperature: {weather.temperature.temp:.1f}°  "
        f"(feels like {weather.temperature.feels_like:.1f}°)",
        f"   Min / Max:   {weather.temperature.temp_min:.1f}° / "
        f"{weather.temperature.temp_max:.1f}°",
        f"   Humidity:    {weather.temperature.humidity}%",
        f"   Pressure:    {weather.temperature.pressure} hPa",
        f"   Wind:        {weather.wind.speed:.1f} m/s, "
        f"{weather.wind.deg}°",
        f"   Visibility:  {weather.visibility} m",
        f"   Clouds:      {weather.clouds}%",
        f"   Observed at: {timestamp_to_str(weather.dt, weather.timezone)}",
    ]
    return TextContent(type="text", text="\n".join(lines))


async def _handle_forecast(service: WeatherService, args: dict) -> TextContent:
    city = args.get("city")
    lat = args.get("lat")
    lon = args.get("lon")
    units = args.get("units", "metric")
    periods = args.get("periods", 8)

    forecast = await service.get_forecast(
        city=city, lat=lat, lon=lon, units=units, periods=periods
    )

    lines = [
        f"📅  **Forecast for {forecast.city}, {forecast.country}** "
        f"({len(forecast.entries)} periods)"
    ]
    for entry in forecast.entries:
        lines.append(
            f"   {timestamp_to_str(entry.dt)} — "
            f"{entry.condition.description.capitalize()}, "
            f"{entry.temperature.temp:.1f}°C, "
            f"💧 {entry.pop * 100:.0f}%"
        )
    return TextContent(type="text", text="\n".join(lines))

