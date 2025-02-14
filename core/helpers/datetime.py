import datetime

def utcnow() -> datetime:
    """Return the current UTC datetime."""
    return datetime.datetime.now(datetime.timezone.utc)
