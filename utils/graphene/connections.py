"""graphene relay connections."""
from graphene import Connection, Int


class PageConnection(Connection):
    """Page Connection.

    Connection to support to total count, edge count.
    """

    class Meta:
        """PageConnection meta."""

        abstract = True

    total_count = Int()
    edges_count = Int()

    @classmethod
    def resolve_total_count(cls, root, info, **kwargs):
        """Total count at queryset."""
        return root.length

    @classmethod
    def resolve_edges_count(cls, root, info, **kwargs):
        """Row count at pagination queryset."""
        return len(root.edges)
