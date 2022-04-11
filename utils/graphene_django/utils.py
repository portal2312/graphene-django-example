"""graphene base."""
import importlib

from django.conf import settings


def get_settings_graphene_schema():
    """Get django settings graphene schema."""
    settings_graphene_schema = settings.GRAPHENE.get("SCHEMA")
    if not settings_graphene_schema:
        raise KeyError(
            "Define the schema location for Graphene in the settings.py file of your Django project: "
            "https://docs.graphene-python.org/projects/django/en/latest/installation/"
        )
    module_name, schema_attr_name = settings_graphene_schema.rsplit(".", 1)
    module = importlib.import_module(module_name)
    return getattr(module, schema_attr_name, None)


def execute_graphql_query(query, **variables):
    """Execute graphql query."""
    schema = get_settings_graphene_schema()

    if "pageSize" not in variables:
        variables["pageSize"] = settings.GRAPHENE["RELAY_CONNECTION_MAX_LIMIT"]

    return schema.execute(
        query,
        **{
            "variable_values": variables,
        },
    )
