from fastapi import APIRouter, status
from pymongo.errors import DuplicateKeyError

from app.models import Subscriber
from app.schemas import SubscriberIn

router = APIRouter(prefix="/api")


@router.post("/subscribers", status_code=status.HTTP_202_ACCEPTED)
async def subscribe(body: SubscriberIn) -> dict[str, str]:
    """Newsletter signup. Same response for new and repeat addresses, so the
    endpoint can't be used to check who is on the list."""
    try:
        await Subscriber(email=body.email.lower()).insert()
    except DuplicateKeyError:
        pass
    return {"status": "ok"}
