"""graphene-django types."""
from graphene import Int, JSONString, ObjectType


class DjangoModelDeleteType(ObjectType):
    """Model delete result type."""

    count = Int(required=True)
    deleted = JSONString(required=True)
