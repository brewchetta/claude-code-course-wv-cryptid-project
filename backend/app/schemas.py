from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class SubscriberIn(BaseModel):
    email: EmailStr


class SightingIn(BaseModel):
    cryptid_code: str = Field(min_length=1, max_length=20)
    occurred_at: datetime
    location_text: str = Field(min_length=1, max_length=200)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    description: str = Field(min_length=10, max_length=5000)
    reporter_type: Literal["west_virginian", "out_of_state", "undisclosed"] = "undisclosed"
    anonymous: bool = True


class SightingOut(BaseModel):
    id: str
    cryptid_code: str
    occurred_at: datetime
    location_text: str
    latitude: float | None
    longitude: float | None
    description: str
    reporter_type: str
    anonymous: bool
    status: str
    created_at: datetime
    conditions: dict | None


class CryptidOut(BaseModel):
    code: str
    name: str
    short: str
    klass: str
    county: str
    county_short: str
    description: str
    first_report: str
