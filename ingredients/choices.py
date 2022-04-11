"""Ingredients choices."""
from django.db.models import TextChoices


class IngredientType(TextChoices):
    """음식 종류."""

    VEGETABLE = ("vegetable", "채소")
    MEAT = ("meat", "육류")
    COMPLEX = ("complex", "복합")
