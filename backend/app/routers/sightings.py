import secrets
from typing import Literal

from beanie import PydanticObjectId
from fastapi import APIRouter, BackgroundTasks, Header, HTTPException, Query, Request, status

from app.config import settings
from app.models import Cryptid, GeoPoint, Sighting
from app.schemas import SightingIn, SightingOut
from app.services.conditions import attach_conditions

router = APIRouter(prefix="/api")


def to_out(s: Sighting) -> SightingOut:
    coords = s.location.coordinates if s.location else None
    return SightingOut(
        id=str(s.id),
        cryptid_code=s.cryptid_code,
        occurred_at=s.occurred_at,
        location_text=s.location_text,
        latitude=coords[1] if coords else None,
        longitude=coords[0] if coords else None,
        description=s.description,
        reporter_type=s.reporter_type,
        anonymous=s.anonymous,
        status=s.status,
        created_at=s.created_at,
        conditions=s.conditions,
    )


def require_admin(x_admin_key: str | None) -> None:
    if not settings.admin_key:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Moderation is not configured")
    if not x_admin_key or not secrets.compare_digest(x_admin_key, settings.admin_key):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Bad admin key")


@router.get("/sightings", response_model=list[SightingOut])
async def list_sightings(
    cryptid: str | None = None,
    limit: int = Query(50, ge=1, le=200),
) -> list[SightingOut]:
    """Approved sightings, newest first."""
    query = Sighting.find(Sighting.status == "approved")
    if cryptid:
        query = query.find(Sighting.cryptid_code == cryptid)
    found = await query.sort(-Sighting.occurred_at).limit(limit).to_list()
    return [to_out(s) for s in found]


@router.post("/sightings", response_model=SightingOut, status_code=status.HTTP_201_CREATED)
async def submit_sighting(
    body: SightingIn, request: Request, background: BackgroundTasks
) -> SightingOut:
    """Public submission. Always lands in the moderation queue as `pending`.
    Moon and weather for the time and place are attached afterwards, in the background."""
    code = body.cryptid_code.upper()
    if code != "UNKNOWN" and not await Cryptid.find_one(Cryptid.code == code):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Unknown cryptid code")

    if (body.latitude is None) != (body.longitude is None):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "Send both latitude and longitude, or neither"
        )
    location = (
        GeoPoint(coordinates=(body.longitude, body.latitude))
        if body.latitude is not None and body.longitude is not None
        else None
    )

    sighting = Sighting(
        cryptid_code=code,
        occurred_at=body.occurred_at,
        location_text=body.location_text,
        location=location,
        description=body.description,
        reporter_type=body.reporter_type,
        anonymous=body.anonymous,
    )
    await sighting.insert()
    background.add_task(attach_conditions, request.app.state.http, sighting.id)
    return to_out(sighting)


@router.get("/admin/sightings", response_model=list[SightingOut])
async def moderation_queue(
    sighting_status: Literal["pending", "approved", "rejected"] = Query("pending", alias="status"),
    x_admin_key: str | None = Header(default=None),
) -> list[SightingOut]:
    require_admin(x_admin_key)
    found = await Sighting.find(Sighting.status == sighting_status).sort(Sighting.created_at).to_list()
    return [to_out(s) for s in found]


@router.patch("/admin/sightings/{sighting_id}", response_model=SightingOut)
async def moderate_sighting(
    sighting_id: PydanticObjectId,
    new_status: Literal["approved", "rejected"] = Query(alias="status"),
    x_admin_key: str | None = Header(default=None),
) -> SightingOut:
    require_admin(x_admin_key)
    sighting = await Sighting.get(sighting_id)
    if sighting is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such sighting")
    sighting.status = new_status
    await sighting.save()
    return to_out(sighting)
