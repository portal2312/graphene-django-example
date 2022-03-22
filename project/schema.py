"""Graphene Django root schema file for project project."""
import graphene
from graphene import Field, ObjectType
from graphene_django.debug import DjangoDebug


class Query(ObjectType):
    """Root Query."""

    debug = Field(DjangoDebug, name='_debug')
    hello = graphene.String(default_value="Hi!")


schema = graphene.Schema(query=Query)
