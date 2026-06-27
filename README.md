# weather-mcp 🌤

An [MCP (Model Context Protocol)](https://modelcontextprotocol.io) server that
provides weather data — current conditions and forecasts — to AI agents.

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

what an MCP Server?
An MCP server is just a Python program that:

1. Starts a server.
2. Registers one or more tools.
3. Waits for a client (Cline) to call those tools.
4. Executes the requested tool.
5. Returns the result.