"""Ingredients Models."""
from graphene import ObjectType, relay
from graphene_django.filter import DjangoFilterConnectionField

from .mutations import (
    DeleteCategoryMutation,
    DeleteIngredientMutation,
    SaveCategoryMutation,
    SaveIngredientMutation,
)
from .types import (
    CategoryType,
    IngredientType,
)


class Mutation(ObjectType):
    """Ingredients root mutation."""

    delete_category = DeleteCategoryMutation.Field()
    save_category = SaveCategoryMutation.Field()

    delete_ingredient = DeleteIngredientMutation.Field()
    save_ingredient = SaveIngredientMutation.Field()


class Query(ObjectType):
    """Ingredients root query."""

    category = relay.Node.Field(CategoryType)
    categories = DjangoFilterConnectionField(CategoryType, max_limit=None)

    ingredient = relay.Node.Field(IngredientType)
    ingredients = DjangoFilterConnectionField(IngredientType)
