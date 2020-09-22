"""module for dictof validator."""
from __future__ import annotations
from typing import Any
from inflection import underscore, camelize
from ..fields import FieldDescription, FieldType, CollectionNullability
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator
from ..utils.concat_keypath import concat_keypath
from ..utils.nonnull_note import NonnullNote
from ..types_resolver import resolve_types
from ..contexts import ValidatingContext, TransformingContext


class DictOfValidator(Validator):
    """This validator validates dict."""

    def __init__(self, types: Any) -> None:
        self.types = types

    def define(self, field_description: FieldDescription) -> None:
        field_description.field_type = FieldType.DICT
        field_description.dict_item_types = self.types

    def validate(self, context: ValidatingContext) -> None:
        if context.value is None:
            return
        if not isinstance(context.value, dict):
            raise ValidationException(
                {context.keypath: f'Value \'{context.value}\' at \'{context.keypath}\' should be a dict.'},
                context.root
            )
        types = resolve_types(self.types, context.config.linked_class)
        if types:
            if types.field_description.collection_nullability == CollectionNullability.UNDEFINED:
                types = types.required
            keypath_messages = {}
            for k, v in context.value.items():
                try:
                    item_context = ValidatingContext(
                        value=v,
                        keypath=concat_keypath(context.keypath, k),
                        root=context.root,
                        all_fields=context.all_fields,
                        config=context.config)
                    types.validator.validate(item_context)
                except ValidationException as exception:
                    if context.all_fields:
                        keypath_messages.update(exception.keypath_messages)
                    else:
                        raise exception
            if len(keypath_messages) > 0:
                raise ValidationException(keypath_messages=keypath_messages, root=context.root)

    def transform(self, context: TransformingContext) -> Any:
        if context.value is None:
            return None
        value = {} if isinstance(context.value, NonnullNote) else context.value
        if not isinstance(value, dict):
            return value
        types = resolve_types(self.types, context.config.linked_class)
        if types:
            retval = {}
            for k, v in value.items():
                new_key = underscore(k) if context.config.camelize_json_keys else k
                item_context = TransformingContext(
                    value=v,
                    keypath=concat_keypath(context.keypath, new_key),
                    root=context.root,
                    all_fields=context.all_fields,
                    config=context.config)
                new_value = types.validator.transform(item_context)
                retval[new_key] = new_value
            return retval
        else:
            return value

    def tojson(self, value: Any, config: Config) -> Any:
        if value is None:
            return None
        if type(value) is not dict:
            return value
        types = resolve_types(self.types, config.linked_class)
        if types:
            # flake8: noqa
            return {camelize(k, False) if config.camelize_json_keys else k: types.validator.tojson(v, config) for k, v in value.items()}
        else:
            return value
