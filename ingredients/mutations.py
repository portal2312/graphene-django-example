"""Ingredients mutations.

https://docs.graphene-python.org/projects/django/en/latest/mutations/#djangomodelformmutation
"""
from graphene import Boolean, Field
from graphql import GraphQLError

from utils.graphene_django.mutations import (
    DjangoModelDeleteMutation,
    RelayDjangoModelFormMutation,
)

from .forms import CategoryForm, IngredientForm
from .models import Category, Ingredient
from .types import CategoryType, IngredientType
from .decorators import logit


class SaveCategoryMutation(RelayDjangoModelFormMutation):
    """Category mutation."""

    category = Field(
        CategoryType,
        description=CategoryType.__doc__,
    )

    class Meta:
        """Category mutation meta."""

        # graphql mutation input 을 자동 완성, Django ModelForm validate 지원합니다.
        form_class = CategoryForm


class SaveIngredientMutation(RelayDjangoModelFormMutation):
    """Ingredient mutation."""

    ingredient = Field(
        IngredientType,
        description=IngredientType.__doc__,
    )

    class Meta:
        """Ingredient mutation meta."""

        form_class = IngredientForm

    class Input:
        """Others input fields."""

        # form_class 로 부터 자동 생성된 input 안에 추가됩니다.
        # https://docs.graphene-python.org/projects/django/en/latest/mutations/#relay

        do_not_save = Boolean(
            default_value=False,
            description="저장 여부",
        )

    @classmethod
    def perform_mutate(cls, form, info):
        """Override.

        https://docs.djangoproject.com/en/4.0/topics/forms/modelforms/#the-save-method
        https://docs.graphene-python.org/projects/django/en/latest/mutations/#form-validation
        """
        # 별도로 추가된 input 값을 활용할 수 있습니다.
        if form.data.get("do_not_save"):
            raise GraphQLError("저장하지 않기")

        obj = form.save(commit=False)
        obj.save()  # Create or Update.

        kwargs = {
            # form_class 를 참조 받아 자동으로 생성된 field 에 obj 대입하기.
            cls._meta.return_field_name: obj,
        }
        return cls(errors=[], **kwargs)


class DeleteCategoryMutation(DjangoModelDeleteMutation):
    """Category delete mutation."""

    class Meta:
        """Cluster delete mutation meta."""

        model = Category


class DeleteIngredientMutation(DjangoModelDeleteMutation):
    """Ingredient delete mutation."""

    class Meta:
        """Ingredient delete mutation meta."""

        model = Ingredient

    @classmethod
    @logit
    def perform_mutate(cls, qs, info, **input):
        """Override."""
        return super().perform_mutate(qs, info, **input)
