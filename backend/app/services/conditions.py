"""Moon + weather for a place and time: snapshots for sightings and the live reading."""

import asyncio
import logging
import time
from datetime import datetime, timezone

import httpx
from beanie import PydanticObjectId

from app.models import GeoPoint, Sighting
from app.services import moon, weather
from app.services.geocode import geocode_wv
from app.services.timeutil import WV_TZ, to_wv_local

log = logging.getLogger(__name__)


async def build_snapshot(client: httpx.AsyncClient, local_dt: datetime, lat: float, lon: float) -> dict:
    """Moon and weather for `local_dt` at a point. Weather is None if Open-Meteo is
    unreachable; the moon always has a value (local fallback)."""
    moon_result, weather_result = await asyncio.gather(
        moon.get_moon(client, local_dt, lat, lon),
        weather.get_weather_at(client, local_dt, lat, lon),
        return_exceptions=True,
    )
    if isinstance(weather_result, BaseException):
        log.warning("weather lookup failed: %s", weather_result)
        weather_result = None
    if isinstance(moon_result, BaseException):  # get_moon already falls back; belt and braces
        moon_result = moon.local_moon(local_dt)
    return {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "moon": moon_result,
        "weather": weather_result,
    }


async def attach_conditions(client: httpx.AsyncClient, sighting_id: PydanticObjectId) -> None:
    """Background task: fill in a sighting's conditions after it has been saved, so
    a slow or failing outside API never blocks or fails a submission."""
    try:
        sighting = await Sighting.get(sighting_id)
        if sighting is None:
            return

        updates: dict = {}
        if sighting.location:
            lon, lat = sighting.location.coordinates
            place_name, location_source = sighting.location_text, "submitted"
        else:
            place = await geocode_wv(client, sighting.location_text)
            if place is None:
                log.info("no West Virginia match for %r, skipping conditions", sighting.location_text)
                return
            lat, lon = place.latitude, place.longitude
            place_name, location_source = place.name, "geocoded"
            updates["location"] = GeoPoint(coordinates=(lon, lat)).model_dump()

        snapshot = await build_snapshot(client, to_wv_local(sighting.occurred_at), lat, lon)
        snapshot["location"] = {
            "name": place_name,
            "latitude": lat,
            "longitude": lon,
            "source": location_source,
        }
        updates["conditions"] = snapshot
        await sighting.set(updates)
    except Exception:
        log.exception("could not attach conditions to sighting %s", sighting_id)


class LiveConditions:
    """The current moon and weather at one point, cached so page views never reach
    the outside APIs directly."""

    def __init__(self, ttl_seconds: int = 600):
        self._ttl = ttl_seconds
        self._value: dict | None = None
        self._stored_at = 0.0
        self._lock = asyncio.Lock()

    async def get(self, client: httpx.AsyncClient, lat: float, lon: float, label: str) -> dict:
        async with self._lock:
            if self._value and time.monotonic() - self._stored_at < self._ttl:
                return self._value

            now = datetime.now(WV_TZ)
            moon_result, weather_result = await asyncio.gather(
                moon.get_moon(client, now, lat, lon),
                weather.get_current_weather(client, lat, lon),
                return_exceptions=True,
            )
            if isinstance(weather_result, BaseException):
                log.warning("current weather lookup failed: %s", weather_result)
                if self._value and self._value.get("weather"):
                    weather_result = self._value["weather"]  # keep the last good reading
                else:
                    weather_result = None
            if isinstance(moon_result, BaseException):
                moon_result = moon.local_moon(now)

            self._value = {
                "location": label,
                "latitude": lat,
                "longitude": lon,
                "moon": moon_result,
                "weather": weather_result,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
            self._stored_at = time.monotonic()
            return self._value
