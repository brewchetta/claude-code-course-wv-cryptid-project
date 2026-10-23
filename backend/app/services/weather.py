"""Weather from Open-Meteo (keyless, free for non-commercial use, CC BY 4.0)."""

from datetime import datetime

import httpx

from app.services.timeutil import WV_TZ

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"

HOURLY = "temperature_2m,cloud_cover,visibility,pressure_msl,wind_speed_10m,precipitation,weather_code"
CURRENT = "temperature_2m,cloud_cover,visibility,pressure_msl,wind_speed_10m,precipitation,weather_code"

# The archive lags real time by several days; the forecast API covers the recent past.
ARCHIVE_AFTER_DAYS = 7

UNITS = {
    "temperature_unit": "fahrenheit",
    "wind_speed_unit": "mph",
    "precipitation_unit": "inch",
    "timezone": "America/New_York",
}


def describe_code(code: int | None) -> str | None:
    """WMO weather interpretation code to words."""
    if code is None:
        return None
    if code == 0:
        return "Clear"
    if code in (1, 2):
        return "Partly cloudy"
    if code == 3:
        return "Overcast"
    if code in (45, 48):
        return "Fog"
    if 51 <= code <= 57:
        return "Drizzle"
    if 61 <= code <= 67 or 80 <= code <= 82:
        return "Rain"
    if 71 <= code <= 77 or code in (85, 86):
        return "Snow"
    if code >= 95:
        return "Thunderstorm"
    return None


def _reading(values: dict, source: str) -> dict:
    return {
        "temperature_f": values.get("temperature_2m"),
        "cloud_cover_pct": values.get("cloud_cover"),
        "visibility_m": values.get("visibility"),
        "pressure_hpa": values.get("pressure_msl"),
        "wind_mph": values.get("wind_speed_10m"),
        "precip_in": values.get("precipitation"),
        "summary": describe_code(values.get("weather_code")),
        "source": source,
    }


async def get_weather_at(client: httpx.AsyncClient, local_dt: datetime, lat: float, lon: float) -> dict:
    """Conditions in the hour of `local_dt` (West Virginia local time)."""
    day = local_dt.date()
    age_days = (datetime.now(WV_TZ).date() - day).days
    url = ARCHIVE_URL if age_days >= ARCHIVE_AFTER_DAYS else FORECAST_URL
    res = await client.get(
        url,
        params={
            "latitude": lat,
            "longitude": lon,
            "hourly": HOURLY,
            "start_date": day.isoformat(),
            "end_date": day.isoformat(),
            **UNITS,
        },
    )
    res.raise_for_status()
    hourly = res.json()["hourly"]
    hour = local_dt.hour
    values = {name: series[hour] for name, series in hourly.items() if name != "time"}
    return _reading(values, "open-meteo-archive" if url == ARCHIVE_URL else "open-meteo")


async def get_current_weather(client: httpx.AsyncClient, lat: float, lon: float) -> dict:
    res = await client.get(
        FORECAST_URL,
        params={"latitude": lat, "longitude": lon, "current": CURRENT, **UNITS},
    )
    res.raise_for_status()
    return _reading(res.json()["current"], "open-meteo")
