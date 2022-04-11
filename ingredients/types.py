"""Ingredients Nodes."""
from graphene import Int, String, relay
from graphene_django import DjangoObjectType

from utils.graphene.connections import PageConnection

from .filtersets import IngredientFilterSet
from .models import Category, Ingredient
from .resolvers import resolve_create_time_isoformat


class CategoryType(DjangoObjectType):
    """Category Type."""

    pk = Int(description="Primary key")

    class Meta:
        """Category Type meta."""

        model = Category
        interfaces = (relay.Node,)  # MUST requirements for "filter_fields".
        filter_fields = ["name"]  # Set simple filter.
        connection_class = PageConnection


class IngredientType(DjangoObjectType):
    """Ingredient Type."""

    pk = Int(description="Primary key")  # pk field 추가시 자동으로 값이 추가된다.
    create_time_str = String(description="생성 일시")

    class Meta:
        """Ingredient Type meta."""

        model = Ingredient
        interfaces = (relay.Node,)
        filterset_class = IngredientFilterSet  # Set complex filter.
        connection_class = PageConnection

    resolve_create_time_str = resolve_create_time_isoformat
