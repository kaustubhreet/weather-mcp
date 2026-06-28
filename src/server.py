"""
MCP server entry point for weather-mcp.

Run with:
    python -m src.server
or with the MCP CLI:
    mcp run src/server.py
"""

import asyncio
import logging
from typing import Any

from mcp.server import Server,NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server

from src.config import MCP_SERVER_NAME, MCP_SERVER_VERSION
from src.logger import logger, setup_logging
from src.services.weather_service import WeatherService
from src.tools.weather import register_tools

import inspect
import mcp

print("MCP location:", inspect.getfile(mcp))
async def main():
    try:
        service = WeatherService()

        server = Server(
            MCP_SERVER_NAME,
            version=MCP_SERVER_VERSION,
        )

        register_tools(server, service)

        initialization_options = InitializationOptions(
            server_name=MCP_SERVER_NAME,
            server_version=MCP_SERVER_VERSION,
            capabilities=server.get_capabilities(
                notification_options=NotificationOptions(),
                experimental_capabilities={},
            ),
        )

        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                initialization_options,
                raise_exceptions=True,
            )
    except Exception:
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    asyncio.run(main())
