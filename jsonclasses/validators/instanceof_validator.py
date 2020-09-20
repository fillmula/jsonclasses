"""module for instanceof validator."""
from __future__ import annotations
from typing import Any
from ..field_description import FieldDescription, FieldType
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator
from ..utils.keypath import keypath
from ..fields import collection_argument_type_to_types, fields
from ..field_description import WriteRule, ReadRule


class InstanceOfValidator(Validator):
    """This validator validates JSON Class instance."""

    def __init__(self, types) -> None:
        self.types = types

    def define(self, field_description: FieldDescription) -> None:
        field_description.field_type = FieldType.INSTANCE
        field_description.instance_types = self.types

    def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> None:
        if value is None:
            return
        keypath_messages = {}
        for field in fields(value):
            if field.field_types:
                field_types = field.field_types
                field_name = field.field_name
                field_value = getattr(value, field_name)
                try:
                    field_types.validator.validate(field_value, keypath(key_path, field_name), root, all_fields, config)
                except ValidationException as exception:
                    if all_fields:
                        keypath_messages.update(exception.keypath_messages)
                    else:
                        raise exception
        if len(keypath_messages) > 0:
            raise ValidationException(keypath_messages=keypath_messages, root=root)

    # pylint: disable=arguments-differ, too-many-locals, too-many-branches
    def transform(
        self,
        value: Any,
        key_path: str,
        root: Any,
        all_fields: bool,
        config: Config,
        base: Any = None,
        fill_blanks: bool = True
    ):
        from ..types import Types
        if value is None:
            return None if not base else base
        if not isinstance(value, dict):
            return value if not base else base
        types = collection_argument_type_to_types(self.types, config.linked_class)
        cls = types.field_description.instance_types
        assert cls is not None
        if not base:
            base = cls(__empty__=True)

        def fill_blank_with_default_value(field):
            if field.assigned_default_value is not None:
                setattr(base, field.field_name, field.assigned_default_value)
            else:
                transformed_field_value = field.field_types.validator.transform(
                    None, keypath(key_path, field.field_name), root, all_fields, config)
                setattr(base, field.field_name, transformed_field_value)
        for field in fields(base):
            if field.json_field_name in value.keys() or field.field_name in value.keys():
                field_value = value.get(field.json_field_name)
                if field_value is None and config.camelize_json_keys:
                    field_value = value.get(field.field_name)
                if field.field_types.field_description.write_rule == WriteRule.NO_WRITE:
                    if fill_blanks:
                        fill_blank_with_default_value(field)
                elif field.field_types.field_description.write_rule == WriteRule.WRITE_ONCE:
                    current_field_value = getattr(base, field.field_name)
                    if current_field_value is None or isinstance(current_field_value, Types):
                        transformed_field_value = field.field_types.validator.transform(
                            field_value, keypath(key_path, field.field_name), root, all_fields, config)
                        setattr(base, field.field_name, transformed_field_value)
                    else:
                        if fill_blanks:
                            fill_blank_with_default_value(field)
                else:
                    transformed_field_value = field.field_types.validator.transform(
                        field_value, keypath(key_path, field.field_name), root, all_fields, config)
                    setattr(base, field.field_name, transformed_field_value)
            else:
                if fill_blanks:
                    fill_blank_with_default_value(field)
        return base

    def tojson(self, value, config: Config, ignore_writeonly: bool = False):
        if value is None:
            return None
        retval = {}
        for field in fields(value):
            field_value = getattr(value, field.field_name)
            json_field_name = field.json_field_name
            if field.field_types.field_description.read_rule == ReadRule.NO_READ and not ignore_writeonly:
                continue
            retval[json_field_name] = field.field_types.validator.tojson(field_value, config)
        return retval
