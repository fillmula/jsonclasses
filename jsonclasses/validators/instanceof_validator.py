"""module for instanceof validator."""
from __future__ import annotations
from typing import Any, Type, Union, cast, TYPE_CHECKING
from ..fields import (FieldDescription, FieldStorage, FieldType, WriteRule,
                      ReadRule, Strictness, fields)
from ..exceptions import ValidationException
from .validator import Validator
from ..utils.concat_keypath import concat_keypath
from ..types_resolver import resolve_types
from ..contexts import ValidatingContext, TransformingContext, ToJSONContext
if TYPE_CHECKING:
    from ..json_object import JSONObject
    from ..types import Types
    InstanceOfType = Union[Types, str, Type[JSONObject]]


class InstanceOfValidator(Validator):
    """InstanceOf validator validates and transforms JSON Class instance."""

    def __init__(self, raw_type: InstanceOfType) -> None:
        self.raw_type = raw_type

    def define(self, field_description: FieldDescription) -> None:
        field_description.field_type = FieldType.INSTANCE
        field_description.instance_types = self.raw_type

    def validate(self, context: ValidatingContext) -> None:
        from ..json_object import JSONObject
        if context.value is None:
            return
        types = resolve_types(self.raw_type, context.config_owner.linked_class)
        cls = cast(Type[JSONObject], types.field_description.instance_types)
        if not isinstance(context.value, cls):
            raise ValidationException({
                context.keypath_root: (f"Value at '{context.keypath_root}' "
                                       f"should be instance of "
                                       f"'{cls.__name__}'.")
            }, context.root)
        keypath_messages = {}
        for field in fields(context.value):
            field_name = field.field_name
            try:
                field.field_types.validator.validate(context.new(
                    value=getattr(context.value, field_name),
                    keypath_root=concat_keypath(context.keypath_root,
                                                field_name),
                    keypath_owner=field_name,
                    owner=context.value,
                    config_owner=context.value.__class__.config,
                    keypath_parent=field_name,
                    parent=context.value,
                    field_description=field.field_description))
            except ValidationException as exception:
                if context.all_fields:
                    keypath_messages.update(exception.keypath_messages)
                else:
                    raise exception
        if len(keypath_messages) > 0:
            raise ValidationException(keypath_messages=keypath_messages, root=context.root)

    def _strictness_check(self,
                          context: TransformingContext,
                          dest: JSONObject) -> None:
        if context.config_owner.camelize_json_keys:
            available_name_pairs = [(field.field_name, field.json_field_name)
                                    for field in fields(dest)]
            available_names = [e for pair in available_name_pairs for e in pair]
        else:
            available_names = [field.field_name for field in fields(dest)]
        for k in context.value.keys():
            if k not in available_names:
                raise ValidationException(
                    {context.keypath_root: f'Key \'{k}\' at \'{context.keypath_root}\' is now allowed.'},
                    context.root)

    # pylint: disable=arguments-differ, too-many-locals, too-many-branches
    def transform(self, context: TransformingContext) -> Any:
        from ..types import Types
        from ..json_object import JSONObject
        if context.value is None:
            return context.dest if context.dest is not None else None
        if not isinstance(context.value, dict):
            return context.value if not context.dest else context.dest
        types = resolve_types(self.raw_type, context.config_owner.linked_class)
        cls = cast(Type[JSONObject], types.field_description.instance_types)
        dest = context.dest if context.dest is not None else cls(_empty=True)

        # strictness check
        strictness = False
        if context.field_description is not None:
            if context.field_description.strictness == Strictness.STRICT:
                strictness = True
            elif context.field_description.strictness == Strictness.UNSTRICT:
                strictness = False
            else:
                strictness = cast(bool, cls.config.strict_input)
        else:
            strictness = context.config_owner.strict_input or False
        if strictness:
            self._strictness_check(context, dest)

        def fill_blank_with_default_value(field):
            if field.assigned_default_value is not None:
                setattr(dest, field.field_name, field.assigned_default_value)
            else:
                tsfmd = field.field_types.validator.transform(context.new(
                    value=None,
                    keypath_root=concat_keypath(context.keypath_root, field.field_name),
                    keypath_owner=field.field_name,
                    owner=context.value,
                    config_owner=cls.config,
                    keypath_parent=field.field_name,
                    parent=context.value,
                    field_description=field.field_description))
                setattr(dest, field.field_name, tsfmd)
        for field in fields(dest):
            if field.json_field_name in context.value.keys() or field.field_name in context.value.keys():
                field_value = context.value.get(field.json_field_name)
                if field_value is None and context.config_owner.camelize_json_keys:
                    field_value = context.value.get(field.field_name)
                if field.field_description.write_rule == WriteRule.NO_WRITE:
                    if context.fill_dest_blanks:
                        fill_blank_with_default_value(field)
                elif field.field_description.write_rule == WriteRule.WRITE_ONCE:
                    current_field_value = getattr(dest, field.field_name)
                    if current_field_value is None or isinstance(current_field_value, Types):
                        field_context = context.new(
                            value=field_value,
                            keypath_root=concat_keypath(context.keypath_root,
                                                        field.field_name),
                            keypath_owner=field.field_name,
                            owner=context.value,
                            config_owner=cls.config,
                            keypath_parent=field.field_name,
                            parent=context.value,
                            field_description=field.field_description)
                        transformed = field.field_types.validator.transform(
                            field_context)
                        setattr(dest, field.field_name, transformed)
                    else:
                        if context.fill_dest_blanks:
                            fill_blank_with_default_value(field)
                else:
                    field_context = context.new(
                        value=field_value,
                        keypath_root=concat_keypath(context.keypath_root,
                                                    field.field_name),
                        keypath_owner=field.field_name,
                        owner=context.value,
                        config_owner=cls.config,
                        keypath_parent=field.field_name,
                        parent=context.value,
                        field_description=field.field_description)
                    transformed = field.field_types.validator.transform(
                        field_context)
                    if field.field_description.field_storage == FieldStorage.FOREIGN_KEY:
                        fk = field.field_description.foreign_key
                        assert fk is not None
                        if field.field_description.field_type == FieldType.LIST:
                            object_fields = fields(transformed[0])
                            try:
                                object_field = next(f for f in object_fields
                                                    if f.field_name == fk)
                            except StopIteration:
                                raise ValueError('Unmatched link reference.')
                            for t_item in transformed:
                                if object_field.field_description.field_type == FieldType.LIST:
                                    setattr(t_item, fk, [dest])
                                else:
                                    setattr(t_item, fk, dest)
                        else:
                            object_fields = fields(transformed)
                            try:
                                object_field = next(f for f in object_fields
                                                    if f.field_name == fk)
                            except StopIteration:
                                raise ValueError('Unmatched link reference.')
                            if object_field.field_description.field_type == FieldType.LIST:
                                setattr(transformed, fk, [dest])
                            else:
                                setattr(transformed, fk, dest)

                    elif field.field_description.field_storage == FieldStorage.LOCAL_KEY:
                        if field.field_description.field_type == FieldType.LIST:
                            if len(transformed) > 0:
                                object_fields = fields(transformed[0])
                                try:
                                    object_field = next(f for f in object_fields
                                                        if f.field_description.foreign_key == field.field_name)
                                    for i_item in transformed:
                                        if object_field.field_description.field_type == FieldType.LIST:
                                            setattr(i_item, object_field.field_name, [dest])
                                        else:
                                            setattr(i_item, object_field.field_name, dest)
                                except StopIteration:
                                    pass
                        else:
                            object_fields = fields(transformed)
                            try:
                                object_field = next(f for f in object_fields
                                                    if f.field_description.foreign_key == field.field_name)
                                val = getattr(transformed, object_field.field_name)
                                if val is not None and val != context.value:
                                    raise ValueError('Reference value not match.')
                                if object_field.field_description.field_type == FieldType.LIST:
                                    setattr(transformed, object_field.field_name, [dest])
                                else:
                                    setattr(transformed, object_field.field_name, dest)
                            except StopIteration:
                                pass
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
            item_context = context.new(value=field_value)
            retval[json_field_name] = field.field_types.validator.tojson(item_context)
        return retval
