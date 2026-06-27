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

from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.config import MCP_SERVER_NAME, MCP_SERVER_VERSION
from src.logger import logger, setup_logging
from src.services.weather_service import WeatherService
from src.tools.weather import register_tools


async def main() -> None:
    """Start the MCP weather server over stdio."""
    setup_logging(logging.DEBUG)
    logger.info(
        "Starting %s v%s", MCP_SERVER_NAME, MCP_SERVER_VERSION
    )

    service = WeatherService()
    server = Server(MCP_SERVER_NAME, version=MCP_SERVER_VERSION)

    register_tools(server, service)

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream=read_stream,
            write_stream=write_stream,
            server=server,
            initialization_options={},
        )


if __name__ == "__main__":
    asyncio.run(main())

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather MCP")
import tools  # noqa: F401 - registers the tools



@mcp.tool()
def hello_world() -> str:
    """Return a hello message."""
    return "Hello from Weather MCP!"


if __name__ == "__main__":
    mcp.run()