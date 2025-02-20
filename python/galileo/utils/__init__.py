from datetime import datetime, timezone


def _get_timestamp() -> datetime:
    return datetime.now(timezone.utc)
