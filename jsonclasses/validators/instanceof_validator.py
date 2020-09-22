"""module for instanceof validator."""
from __future__ import annotations
from typing import Any
from ..fields import FieldDescription, FieldType, WriteRule, ReadRule, fields
from ..exceptions import ValidationException
from .validator import Validator
from ..utils.concat_keypath import concat_keypath
from ..types_resolver import resolve_types
from ..contexts import ValidatingContext, TransformingContext, ToJSONContext


class InstanceOfValidator(Validator):
    """This validator validates JSON Class instance."""

    def __init__(self, types) -> None:
        self.types = types

    def define(self, field_description: FieldDescription) -> None:
        field_description.field_type = FieldType.INSTANCE
        field_description.instance_types = self.types

    def validate(self, context: ValidatingContext) -> None:
        if context.value is None:
            return
        keypath_messages = {}
        for field in fields(context.value):
            if field.field_types:
                field_types = field.field_types
                field_name = field.field_name
                field_value = getattr(context.value, field_name)
                try:
                    field_context = ValidatingContext(
                        value=field_value,
                        keypath=concat_keypath(context.keypath, field_name),
                        root=context.root,
                        all_fields=context.all_fields,
                        config=context.config,
                        field_description=field.field_description)
                    field_types.validator.validate(field_context)
                except ValidationException as exception:
                    if context.all_fields:
                        keypath_messages.update(exception.keypath_messages)
                    else:
                        raise exception
        if len(keypath_messages) > 0:
            raise ValidationException(keypath_messages=keypath_messages, root=context.root)

    # pylint: disable=arguments-differ, too-many-locals, too-many-branches
    def transform(self, context: TransformingContext) -> Any:
        from ..types import Types
        if context.value is None:
            return context.dest if context.dest is not None else None
        if not isinstance(context.value, dict):
            return context.value if not context.dest else context.dest
        types = resolve_types(self.types, context.config.linked_class)
        cls = types.field_description.instance_types
        assert cls is not None
        dest = context.dest if context.dest is not None else cls(__empty__=True)

        def fill_blank_with_default_value(field):
            if field.assigned_default_value is not None:
                setattr(dest, field.field_name, field.assigned_default_value)
            else:
                transform_context = TransformingContext(
                    value=None,
                    keypath=concat_keypath(context.keypath, field.field_name),
                    root=context.root,
                    all_fields=context.all_fields,
                    config=context.config,
                    field_description=field.field_description)
                transformed = field.field_types.validator.transform(
                    transform_context)
                setattr(dest, field.field_name, transformed)
        for field in fields(dest):
            if field.json_field_name in context.value.keys() or field.field_name in context.value.keys():
                field_value = context.value.get(field.json_field_name)
                if field_value is None and context.config.camelize_json_keys:
                    field_value = context.value.get(field.field_name)
                if field.field_types.field_description.write_rule == WriteRule.NO_WRITE:
                    if context.fill_dest_blanks:
                        fill_blank_with_default_value(field)
                elif field.field_types.field_description.write_rule == WriteRule.WRITE_ONCE:
                    current_field_value = getattr(dest, field.field_name)
                    if current_field_value is None or isinstance(current_field_value, Types):
                        field_context = TransformingContext(
                            value=field_value,
                            keypath=concat_keypath(context.keypath, field.field_name),
                            root=context.root,
                            all_fields=context.all_fields,
                            config=context.config,
                            field_description=field.field_description)
                        transformed = field.field_types.validator.transform(
                            field_context)
                        setattr(dest, field.field_name, transformed)
                    else:
                        if context.fill_dest_blanks:
                            fill_blank_with_default_value(field)
                else:
                    field_context = TransformingContext(
                        value=field_value,
                        keypath=concat_keypath(context.keypath, field.field_name),
                        root=context.root,
                        all_fields=context.all_fields,
                        config=context.config,
                        field_description=field.field_description)
                    transformed = field.field_types.validator.transform(
                        field_context)
                    setattr(dest, field.field_name, transformed)
            else:
                if context.fill_dest_blanks:
                    fill_blank_with_default_value(field)
        return dest

    def tojson(self, context: ToJSONContext) -> Any:
        if context.value is None:
            return None
        retval = {}
        for field in fields(context.value):
            field_value = getattr(context.value, field.field_name)
            json_field_name = field.json_field_name
            if field.field_types.field_description.read_rule == ReadRule.NO_READ and not context.ignore_writeonly:
                continue
            item_context = ToJSONContext(
                value=field_value,
                config=context.config,
                ignore_writeonly=context.ignore_writeonly)
            retval[json_field_name] = field.field_types.validator.tojson(item_context)
        return retval
