"""
Logging configuration for the weather-mcp server.
"""

import logging
import sys

logger = logging.getLogger("weather-mcp")

def setup_logging(level: int = logging.INFO) -> None:
    """Configure the root logger with a standard handler and formatter."""
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(level)
    fmt = logging.Formatter(
        "[%(asctime)s] %(levelname)s  %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(fmt)

    logger.setLevel(level)
    logger.addHandler(handler)
    logger.propagate = False

