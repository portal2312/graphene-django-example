"""graphene-django fields."""
from graphene import Int
from graphene_django.filter import DjangoFilterConnectionField


class PageDjangoFilterConnectionField(DjangoFilterConnectionField):
    """Page DjangoFilterConnectionField.

    Supports:
        Arguments: page, page_size.
    """

    def __init__(self, *args, **kwargs):
        """Override."""
        kwargs.setdefault("page", Int(default_value=1, description="Page number."))
        kwargs.setdefault("page_size", Int(description="Row count per page."))
        super().__init__(*args, **kwargs)

    @classmethod
    # pylint: disable=arguments-differ
    def connection_resolver(
        cls,
        resolver,
        connection,
        default_manager,
        queryset_resolver,
        max_limit,
        enforce_first_or_last,
        root,
        info,
        first=None,
        offset=None,
        page=1,
        page_size=0,
        **args,
    ):
        """Override."""
        return super().connection_resolver(
            resolver,
            connection,
            default_manager,
            queryset_resolver,
            max_limit,
            enforce_first_or_last,
            root,
            info,
            first=first or page_size or None,
            offset=offset or ((page - 1) * page_size) or None,
            **args,
        )
