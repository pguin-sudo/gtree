from datetime import UTC, datetime


def get_current_time():
    """Returns the current time in UTC without timezone information."""
    return datetime.now(UTC).replace(tzinfo=None)
