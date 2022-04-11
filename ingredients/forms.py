"""Ingredients forms.

https://docs.djangoproject.com/en/dev/topics/forms/modelforms/
"""
from django.forms import ModelForm

from .models import Category, Ingredient


class CategoryForm(ModelForm):
    """Category ModelForm."""

    class Meta:
        """Category ModelForm meta."""

        model = Category
        fields = "__all__"  # MUST requirements for ModelForm.


class IngredientForm(ModelForm):
    """Ingredient ModelForm."""

    class Meta:
        """Ingredient ModelForm meta."""

        model = Ingredient
        fields = [
            "name",
            "notes",
            "category",
        ]
        # https://docs.djangoproject.com/en/4.0/topics/forms/modelforms/#validation-on-a-modelform
        error_messages = {
            "name": {
                "unique": "중복된 이름입니다.",
            },
        }
