"""graphene input ObjectTypes."""
from graphene import ID, InputField
from graphene.types.inputobjecttype import InputObjectType, InputObjectTypeOptions
from graphene.types.utils import yank_fields_from_attrs
from graphene_django.forms.mutation import fields_for_form


class FormInputObjectTypeOptions(InputObjectTypeOptions):
    """FormInputObjectType Options."""

    form_class = None


class FormInputObjectType(InputObjectType):
    """InputObjectType to support to included form_class at subclass."""

    @classmethod
    # pylint: disable=arguments-differ
    def __init_subclass_with_meta__(
        cls,
        _meta=None,
        form_class=None,
        only_fields=(),
        exclude_fields=(),
        **options,
    ):
        """Override.

        Support to included form_class at subclass.
        """
        if not _meta:
            _meta = FormInputObjectTypeOptions(cls)
        _meta.form_class = form_class

        fields = {}
        if form_class:
            form = form_class()
            input_fields = fields_for_form(form, only_fields, exclude_fields)
            if "id" not in exclude_fields:
                input_fields["id"] = ID()
            fields.update(yank_fields_from_attrs(input_fields, _as=InputField))

        if _meta.fields:
            _meta.fields.update(fields)
        else:
            _meta.fields = fields

        super().__init_subclass_with_meta__(_meta=_meta, **options)

    class Meta:
        """FormInputObjectType meta."""

        abstract = True


# class FormInputObjectType(InputObjectType):
#     """InputObjectType to support to included form_class at subclass."""

#     @classmethod
#     def __init_subclass_with_meta__(
#         cls,
#         container=None,
#         _meta=None,
#         form_class=None,
#         only_fields=(),
#         exclude_fields=(),
#         **options
#     ):
#         """Override."""
#         if not _meta:
#             _meta = InputObjectTypeOptions(cls)

#         fields = OrderedDict()
#         for base in reversed(cls.__mro__):
#             fields.update(yank_fields_from_attrs(base.__dict__, _as=InputField))

#         # NOTE Support to included form_class at subclass
#         if form_class:
#             form = form_class()
#             input_fields = fields_for_form(form, only_fields, exclude_fields)
#             if "id" not in exclude_fields:
#                 input_fields["id"] = ID()
#             fields.update(yank_fields_from_attrs(input_fields, _as=InputField))

#         if _meta.fields:
#             _meta.fields.update(fields)
#         else:
#             _meta.fields = fields
#         if container is None:
#             container = type(cls.__name__, (InputObjectTypeContainer, cls), {})
#         _meta.container = container

#         super().__init_subclass_with_meta__(_meta=_meta, **options)

#     class Meta:
#         """FormInputObjectType meta."""

#         abstract = True
