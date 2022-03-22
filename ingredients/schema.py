"""Ingredients Models."""
from graphene import Field, List, ObjectType, String
from graphene_django import DjangoObjectType

from .models import Category, Ingredient


class CategoryType(DjangoObjectType):
    """Category Type."""

    class Meta:
        """Category Type meta."""
        model = Category
        fields = ("id", "name", "ingredients")


class IngredientType(DjangoObjectType):
    """Ingredient Type."""

    class Meta:
        """Ingredient Type meta."""
        model = Ingredient
        fields = ("id", "name", "notes", "category")


class Query(ObjectType):
    """Ingredients Query."""
    all_ingredients = List(IngredientType)
    category_by_name = Field(CategoryType, name=String(required=True))

    def resolve_all_ingredients(root, info):
        """모든 Ingredient 목록 가져오기."""
        # We can easily optimize query count in the resolve method
        return Ingredient.objects.select_related("category").all()

    def resolve_category_by_name(root, info, name):
        """Category 가져오기."""
        try:
            return Category.objects.get(name=name)
        except Category.DoesNotExist:
            return None
