# weather-mcp 🌤

An [MCP (Model Context Protocol)](https://modelcontextprotocol.io) server that
provides weather data — current conditions and forecasts — to AI agents.

### what an MCP Server?
```
An MCP server is just a Python program that:
1. Starts a server.
2. Registers one or more tools.
3. Waits for a client (Cline) to call those tools.
4. Executes the requested tool.
5. Returns the result.
```
## Architecture

```
weather-mcp/
├── src/
│   ├── server.py              # MCP server entry point
│   ├── config.py              # Config/constants
│   ├── logger.py              # Logging
│   ├── tools/weather.py       # MCP tool definitions
│   ├── services/weather_service.py  # Business logic
│   ├── clients/weather_client.py    # OpenWeatherMap API client
│   ├── models/weather_model.py      # Data models
│   └── utils/helpers.py             # Utility functions
└── tests/test_weather.py
```

## Prerequisites

- Python ≥ 3.10
- An [OpenWeatherMap API key](https://openweathermap.org/api) (free tier)

## Setup

```bash
# Clone and enter the directory
cd weather-mcp

# Create a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure your API key
cp .env.example .env
# Edit .env and set WEATHER_API_KEY=your_key
```

## Usage

### Run the MCP server (stdio mode)

```bash
python -m src.server
```

Or using the MCP CLI:

```bash
mcp run src/server.py
```

## Available Tools

| Tool              | Description                                |
|-------------------|--------------------------------------------|
| `get_current_weather` | Current conditions by city or GPS coordinates |
| `get_forecast`        | 3-hourly forecast by city or GPS coordinates  |

Both tools accept `units` (`metric`, `imperial`, or `standard`).

## Testing

```bash
pytest tests/
```

### Output format
Here's the current weather for **Mumbai** fetched live from the weather-mcp server:

---
**☁️ Mumbai, IN — Broken Clouds**

| Metric | Value |
|--------|-------|
| 🌡 Temperature | **30.1°C** (feels like **35.5°C**) |
| 📊 Min / Max | 30.1°C / 30.1°C |
| 💧 Humidity | **71%** |
| 🌬 Wind | **4.4 m/s** at 255° (WSW) |
| 👁 Visibility | **10,000 m** |
| ☁️ Cloud Cover | **82%** |
| 🔽 Pressure | **1006 hPa** |

---

Notice the **feels-like temperature (35.5°C)** is noticeably higher than the actual 30.1°C — this is due to the high humidity (71%) making it feel much hotter, which is typical for Mumbai's coastal climate.