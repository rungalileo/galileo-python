from datetime import datetime, timezone


def _get_timestamp():
    return datetime.now(timezone.utc)
