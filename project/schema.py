"""Graphene Django root schema file for project project.

https://docs.graphene-python.org/projects/django/en/latest/schema/#adding-to-the-schema
"""
import graphene
from graphene import Field, ObjectType
from graphene_django.debug import DjangoDebug

from ingredients.schema import Mutation as IngredientsMutation
from ingredients.schema import Query as IngredientsQuery


class Mutation(IngredientsMutation, ObjectType):
    """Root mutation."""

    # https://docs.graphene-python.org/projects/django/en/latest/debug/
    debug = Field(DjangoDebug, name="_debug")


class Query(IngredientsQuery, ObjectType):
    """Root query."""

    # https://docs.graphene-python.org/projects/django/en/latest/debug/
    debug = Field(DjangoDebug, name="_debug")


schema = graphene.Schema(mutation=Mutation, query=Query)
