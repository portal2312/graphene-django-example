"""Ingredients models."""
from django.db import models

from .choices import IngredientType


class Category(models.Model):
    """유형."""

    name = models.CharField(max_length=100, unique=True, help_text="유형 명")

    def __str__(self):
        """유형 명."""
        return self.name

    class Meta:
        """Category meta."""

        ordering = ["name"]


class Ingredient(models.Model):
    """재료."""

    name = models.CharField(max_length=100, unique=True, help_text="재료 명")
    notes = models.TextField(help_text="메모")
    category = models.ForeignKey(
        Category,
        related_name="ingredients",
        on_delete=models.CASCADE,
        help_text="유형",
    )
    type = models.CharField(
        max_length=16,
        choices=IngredientType.choices,
        default=IngredientType.COMPLEX,
        help_text=IngredientType.__doc__,
    )
    create_time = models.DateTimeField(auto_now_add=True, help_text="생성 일시")
    update_time = models.DateTimeField(auto_now=True, help_text="변경 일시")

    def __str__(self):
        """재료 명."""
        return self.name

    class Meta:
        """Ingredient meta."""

        ordering = ["name"]
