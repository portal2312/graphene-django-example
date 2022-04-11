"""Ingredients filtersets.

References:
    https://docs.graphene-python.org/projects/django/en/latest/filtering
    https://docs.graphene-python.org/projects/django/en/latest/filtering/#custom-filtersets
    https://docs.graphene-python.org/projects/django/en/latest/filtering/#ordering
    https://django-filter.readthedocs.io/en/latest/index.html
    https://django-filter.readthedocs.io/en/stable/guide/usage.html#filtering-the-primary-qs
    https://django-filter.readthedocs.io/en/stable/ref/filters.html?highlight=orderingfilter#orderingfilter
    https://django-filter.readthedocs.io/en/stable/guide/tips.html#filter-and-lookup-expression-mismatch-in-range-isnull
"""
from django_filters import FilterSet, OrderingFilter, CharFilter

from .models import Ingredient


class IngredientFilterSet(FilterSet):
    """Ingredient FilterSet."""

    # https://django-filter.readthedocs.io/en/stable/ref/filters.html
    category_name = CharFilter(
        field_name="category__name",
        lookup_expr="icontains",
        label="Category name icontains.",
    )

    # https://django-filter.readthedocs.io/en/stable/ref/filters.html?highlight=orderingfilter#orderingfilter
    order = OrderingFilter(
        fields=(
            "name",
            "category",
            "type",
            "create_time",
            ("create_time", "create_time_str"),
        ),
    )

    class Meta:
        """Ingredient FilterSet meta."""

        model = Ingredient
        fields = {
            "name": ["exact", "icontains"],
            "notes": ["icontains"],
            "category": ["exact"],
            "type": ["exact"],
            "create_time": ["gte", "lt", "lte", "range"],
            "update_time": ["gte", "lt", "lte", "range"],
            "category__name": ["icontains"],
        }

    @property
    def qs(self):
        """Override.

        Supports:
            - select_related and prefetch_related.

        https://django-filter.readthedocs.io/en/stable/guide/usage.html#filtering-the-primary-qs
        """
        qs = super().qs
        return qs.select_related(
            "category",
        ).prefetch_related()
