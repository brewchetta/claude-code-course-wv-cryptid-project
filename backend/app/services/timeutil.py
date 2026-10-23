from datetime import datetime
from zoneinfo import ZoneInfo

WV_TZ = ZoneInfo("America/New_York")


def to_wv_local(when: datetime) -> datetime:
    """A naive datetime is the wall-clock time the witness typed, so it is already
    West Virginia local time. An aware one is converted."""
    if when.tzinfo is None:
        return when.replace(tzinfo=WV_TZ)
    return when.astimezone(WV_TZ)
