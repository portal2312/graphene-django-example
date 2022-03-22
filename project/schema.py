"""Graphene Django root schema file for project project."""
import graphene
from graphene import Field, ObjectType
from graphene_django.debug import DjangoDebug

from ingredients.schema import Query as IngredientsQuery


class Query(IngredientsQuery, ObjectType):
    """Root Query."""

    debug = Field(DjangoDebug, name='_debug')


schema = graphene.Schema(query=Query)
