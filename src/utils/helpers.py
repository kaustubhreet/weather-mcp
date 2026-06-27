"""
Helper utilities.
"""

from datetime import datetime, timezone
from typing import Optional


def timestamp_to_str(utc_ts: int, tz_offset: Optional[int] = None) -> str:
    """Convert a UTC epoch timestamp to an ISO‑8601 string, optionally
    shifted by *tz_offset* seconds (the OpenWeather timezone field)."""
    dt = datetime.fromtimestamp(utc_ts, tz=timezone.utc)
    if tz_offset:
        try:
            from datetime import timedelta, timezone as tz

            dt = dt.astimezone(tz(timedelta(seconds=tz_offset)))
        except Exception:
            pass
    return dt.isoformat(sep=" ", timespec="minutes")


def format_temp(temp_c: float) -> str:
    """Format a Celsius temperature for display."""
    return f"{temp_c:.1f}°C"

