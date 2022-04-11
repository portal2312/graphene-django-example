"""Ingredient resolvers."""
from datetime import datetime as dt


def resolve_create_time_isoformat(self, info):
    """Ingredient.create_time field value Convert datetime to isoformat string.

    Supports:
        - Creating return values in rows ahead of time, without dependencies.
        - Download rendered value to file.

    Returns:
        str: ISO format string.
    """
    create_time = getattr(self, "create_time", None)

    if isinstance(create_time, int):
        create_time_str = dt.fromtimestamp(create_time).isoformat(
            sep=" ", timespec="seconds"
        )
    elif isinstance(create_time, dt):
        create_time_str = create_time.isoformat(sep=" ", timespec="seconds")
    else:
        create_time_str = None

    return create_time_str
