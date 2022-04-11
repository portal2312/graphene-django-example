"""graphene-django mutations."""
import binascii
from collections import OrderedDict

from django.core.exceptions import FieldDoesNotExist
from django.db import IntegrityError, transaction
from graphene import ID, ClientIDMutation, Field, InputField, List
from graphene.types.mutation import MutationOptions
from graphene.types.utils import yank_fields_from_attrs
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphene_django.registry import get_global_registry
from graphql import GraphQLError
from graphql_relay import from_global_id

from .types import DjangoModelDeleteType


def _from_global_id(global_id, default=None):
    """The default parameter support to graphql_replay.from_global_id function.

    Args:
        global_id (str): Relay id.
        default (str, optional): Default identity. Defaults to None.

    Returns:
        (str, str): (graphene type, identity)
    """
    try:
        type, pk = from_global_id(global_id)
    except (binascii.Error, TypeError):
        return (None, default)

    return type, pk or default


class RelayDjangoModelFormMutation(DjangoModelFormMutation):
    """Relay DjangoModelFormMutation.

    Support:
        - input 의 field 중 id field 의 값 유형이 relay id 인 경우, model id 로 자동 변환하기.
        - input 의 field 중 외래키 field 의 값 유형이 relay id 인 경우, model id 로 자동 변환하기.
    """

    class Meta:
        """RelayDjangoModelFormMutation meta."""

        abstract = True

    @classmethod
    def get_form_kwargs(cls, root, info, **input):
        """Override."""
        kwargs = {"data": input}
        id = input.pop("id", None)

        if id:
            _, pk = _from_global_id(id, default=id)
            instance = cls._meta.model._default_manager.get(pk=pk)
            kwargs["instance"] = instance

        meta = getattr(cls._meta.model, "_meta")
        for field_name, value in input.items():
            try:
                field = meta.get_field(field_name)
            except FieldDoesNotExist:
                continue

            if field and getattr(field, "foreign_related_fields", None):
                # field is foreign key field.
                _, pk = _from_global_id(value, default=value)
                input[field_name] = pk

        return kwargs


class DeleteMutationOptions(MutationOptions):
    """Delete MutationOptions."""

    model = None
    return_field_name = None


class DjangoModelDeleteMutation(ClientIDMutation):
    """Relay django model delete clientID mutation."""

    class Meta:
        """Meta class."""

        abstract = True

    deleted = Field(DjangoModelDeleteType)

    @classmethod
    # pylint: disable=arguments-differ
    def __init_subclass_with_meta__(cls, model=None, return_field_name=None, **options):
        """Override."""
        # Validate.
        if not model:
            raise Exception("model is required for DjangoModelDeleteMutation")

        registry = get_global_registry()
        model_type = registry.get_type_for_model(model)
        if not model_type:
            raise Exception(f"No type registered for model: {model.__name__}")

        # Create Field in Input.
        input_fields = OrderedDict()
        input_fields["id"] = List(
            ID,
            required=True,
            description="The ID of the object",
        )

        # Create output fields.
        if not return_field_name:
            model_name = model.__name__
            return_field_name = model_name[:1].lower() + model_name[1:]
        output_fields = OrderedDict()
        output_fields[return_field_name] = Field(List(model_type))
        # output_fields["delete"] = Field(DeleteType)

        # Create _meta.
        _meta = DeleteMutationOptions(cls)
        _meta.fields = yank_fields_from_attrs(output_fields, _as=Field)
        _meta.model = model
        _meta.return_field_name = return_field_name

        # Convert Field to InputField in Input.
        input_fields = yank_fields_from_attrs(input_fields, _as=InputField)

        super().__init_subclass_with_meta__(
            _meta=_meta,
            input_fields=input_fields,
            **options,
        )

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        """Override."""
        qs = cls.get_queryset(root, info, **input)

        if not qs:
            raise GraphQLError(
                f"{cls._meta.model._meta.object_name} matching query does not exist."
            )

        return cls.perform_mutate(qs, info, **input)

    @classmethod
    def get_queryset(cls, root, info, **input):
        """Get queryset to delete model instances."""
        input_id_values = input.pop("id", None)

        if input_id_values:
            # Support to relay id.
            id_list = [_from_global_id(id, default=id)[1] for id in input_id_values]
            return cls._meta.model._default_manager.filter(id__in=id_list)

    @classmethod
    def perform_mutate(cls, qs, info, **input):
        """Mutate to delete model instances."""
        output_fields = {
            cls._meta.return_field_name: qs,
        }

        try:
            with transaction.atomic():
                if len(input["id"]) > 1:
                    # Because of raw query performance.
                    count, deleted = qs.first().delete()
                else:
                    count, deleted = qs.delete()
        except IntegrityError as e:
            raise GraphQLError(*e.args) from e

        return cls(deleted={"count": count, "deleted": deleted}, **output_fields)
