"""Turn the town a witness typed into coordinates (Open-Meteo geocoding, keyless)."""

import re
from dataclasses import dataclass

import httpx

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"


@dataclass
class Place:
    name: str
    latitude: float
    longitude: float


def _town(location_text: str) -> str:
    """'Point Pleasant, Mason Co.' -> 'Point Pleasant'."""
    first = location_text.split(",")[0].strip()
    return re.sub(r"\s+(co\.?|county)$", "", first, flags=re.IGNORECASE).strip()


async def geocode_wv(client: httpx.AsyncClient, location_text: str) -> Place | None:
    """First West Virginia match for the town name, or None. Matches outside the
    state are ignored on purpose: a wrong point is worse than no snapshot."""
    town = _town(location_text)
    if not town:
        return None
    res = await client.get(
        GEOCODE_URL, params={"name": town, "count": 10, "language": "en", "format": "json"}
    )
    res.raise_for_status()
    for hit in res.json().get("results") or []:
        if hit.get("country_code") == "US" and hit.get("admin1") == "West Virginia":
            return Place(hit["name"], hit["latitude"], hit["longitude"])
    return None
