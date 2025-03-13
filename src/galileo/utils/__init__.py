from datetime import datetime, timezone


def _get_timestamp() -> datetime:
    return datetime.now(timezone.utc)


def _now_ns() -> int:
    return int(round(_get_timestamp().timestamp() * 1e9))
