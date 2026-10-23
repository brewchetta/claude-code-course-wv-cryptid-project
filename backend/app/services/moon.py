"""Moon phase, illumination and rise/set from the U.S. Naval Observatory API,
with a local calculation (ephem) as a fallback so the moon never fails."""

import logging
from datetime import datetime, timedelta, timezone

import ephem
import httpx

USNO_URL = "https://aa.usno.navy.mil/api/rstt/oneday"

log = logging.getLogger(__name__)


def _phase_name(illumination: float, waxing: bool) -> str:
    if illumination < 3:
        return "New Moon"
    if illumination > 97:
        return "Full Moon"
    if 47 <= illumination <= 53:
        return "First Quarter" if waxing else "Last Quarter"
    if illumination < 47:
        return "Waxing Crescent" if waxing else "Waning Crescent"
    return "Waxing Gibbous" if waxing else "Waning Gibbous"


def local_moon(local_dt: datetime) -> dict:
    """Phase and illumination at the exact instant. No rise/set."""
    utc = local_dt.astimezone(timezone.utc)
    now = ephem.Moon(utc.strftime("%Y/%m/%d %H:%M:%S")).phase
    later = ephem.Moon((utc + timedelta(hours=1)).strftime("%Y/%m/%d %H:%M:%S")).phase
    return {
        "phase": _phase_name(now, waxing=later > now),
        "illumination_pct": round(now),
        "moonrise": None,
        "moonset": None,
        "source": "local",
    }


async def _usno_moon(client: httpx.AsyncClient, local_dt: datetime, lat: float, lon: float) -> dict:
    offset_hours = local_dt.utcoffset().total_seconds() / 3600
    res = await client.get(
        USNO_URL,
        params={
            "date": local_dt.date().isoformat(),
            "coords": f"{lat},{lon}",
            "tz": offset_hours,
            "dst": "false",  # the offset above already includes daylight time
        },
    )
    res.raise_for_status()
    data = res.json()["properties"]["data"]
    times = {m["phen"]: m["time"] for m in data.get("moondata", [])}
    return {
        "phase": data["curphase"],
        "illumination_pct": int(str(data["fracillum"]).rstrip("%")),
        "moonrise": times.get("Rise"),
        "moonset": times.get("Set"),
        "source": "usno",
    }


async def get_moon(client: httpx.AsyncClient, local_dt: datetime, lat: float, lon: float) -> dict:
    """USNO first; any failure or odd response falls back to the local calculation."""
    try:
        return await _usno_moon(client, local_dt, lat, lon)
    except Exception as exc:  # network, HTTP error, or an unexpected payload
        log.warning("USNO moon lookup failed, using local calculation: %s", exc)
        return local_moon(local_dt)
