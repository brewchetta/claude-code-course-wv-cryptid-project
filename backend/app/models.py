from datetime import datetime, timezone
from typing import Literal

import pymongo
from beanie import Document, Indexed
from pydantic import BaseModel, Field


class GeoPoint(BaseModel):
    """GeoJSON Point. Coordinates are [longitude, latitude]."""

    type: Literal["Point"] = "Point"
    coordinates: tuple[float, float]


class Cryptid(Document):
    code: Indexed(str, unique=True)  # e.g. "WV-001"
    name: str
    short: str
    klass: str
    county: str
    county_short: str
    description: str
    first_report: str

    class Settings:
        name = "cryptids"


class Subscriber(Document):
    email: Indexed(str, unique=True)  # stored lowercased
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "subscribers"


class Sighting(Document):
    cryptid_code: Indexed(str)  # a Cryptid.code, or "UNKNOWN" for new entities
    occurred_at: datetime
    location_text: str
    location: GeoPoint | None = None
    description: str
    reporter_type: Literal["west_virginian", "out_of_state", "undisclosed"]
    anonymous: bool = True
    status: Literal["pending", "approved", "rejected"] = "pending"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    # Moon + weather snapshot for the time and place of the sighting.
    # Left empty until the conditions service is built.
    conditions: dict | None = None

    class Settings:
        name = "sightings"
        indexes = [
            [("location", pymongo.GEOSPHERE)],
            [("status", pymongo.ASCENDING), ("occurred_at", pymongo.DESCENDING)],
        ]


DOCUMENT_MODELS = [Cryptid, Sighting, Subscriber]
