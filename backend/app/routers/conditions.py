from fastapi import APIRouter, Request

from app.config import settings

router = APIRouter(prefix="/api")


@router.get("/conditions")
async def current_conditions(request: Request) -> dict:
    """Current moon and weather at the network's reference point. Cached for 10 minutes."""
    return await request.app.state.live.get(
        request.app.state.http,
        settings.conditions_lat,
        settings.conditions_lon,
        settings.conditions_label,
    )
