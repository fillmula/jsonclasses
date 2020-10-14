"""module for listof validator."""
from __future__ import annotations
from typing import Any, Collection, Iterable, TypeVar, Union, cast, TYPE_CHECKING
from ..fields import FieldDescription, Nullability
from ..config import Config
from ..exceptions import ValidationException
from .type_validator import TypeValidator
from ..keypath import concat_keypath
from ..types_resolver import resolve_types
from ..contexts import ValidatingContext, TransformingContext, ToJSONContext
if TYPE_CHECKING:
    from ..json_object import JSONObject
    from ..types import Types

T = TypeVar('T', bound=Collection)


class CollectionTypeValidator(TypeValidator):
    """Base class for collection type validators."""

    def __init__(self, raw_item_types: Any) -> None:
        super().__init__()
        self.raw_item_types = raw_item_types
        self.exact_type = False

    def define(self, fdesc: FieldDescription) -> None:
        super().define(fdesc)
        fdesc.raw_item_types = self.raw_item_types

    def item_types(self, owner_cls: type[JSONObject]) -> Types:
        if hasattr(self, '_item_types'):
            return getattr(self, '_item_types')
        else:
            itypes = resolve_types(self.raw_item_types, owner_cls)
            if itypes.fdesc.item_nullability == Nullability.UNDEFINED:
                itypes = itypes.required
            setattr(self, '_item_types', itypes)
            return itypes

    def enumerator(self, value: Collection) -> Iterable:
        raise NotImplementedError('please implement enumerator')

    def empty_collection(self) -> Collection:
        raise NotImplementedError('please override empty_collection')

    def append_value(self, i: Union[str, int], v: Any, col: Collection):
        raise NotImplementedError('please implement append_value')

    def to_object_key(self, key: T, conf: Config) -> T:
        return key

    def to_json_key(self, key: T, conf: Config) -> T:
        return key

    def validate(self, context: ValidatingContext) -> None:
        if context.value is None:
            return
        super().validate(context)
        types = self.item_types(context.config_owner.linked_class)
        all_fields = next(b for b in [
            context.all_fields,
            context.config_owner.validate_all_fields] if b is not None)
        keypath_messages = {}
        for i, v in self.enumerator(context.value):
            try:
                types.validator.validate(context.new(
                    value=v,
                    keypath_root=concat_keypath(context.keypath_root, i),
                    keypath_owner=concat_keypath(context.keypath_owner, i),
                    keypath_parent=i,
                    parent=context.value,
                    fdesc=types.fdesc))
            except ValidationException as exception:
                if all_fields:
                    keypath_messages.update(exception.keypath_messages)
                else:
                    raise exception
        if len(keypath_messages) > 0:
            raise ValidationException(
                keypath_messages=keypath_messages,
                root=context.root)

    def transform(self, context: TransformingContext) -> Any:
        fdesc = cast(FieldDescription, context.fdesc)
        if context.value is None:
            if fdesc.collection_nullability == Nullability.NONNULL:
                return self.empty_collection()
            else:
                return None
        if not isinstance(context.value, self.cls):
            return context.value
        itypes = self.item_types(context.config_owner.linked_class)
        retval = self.empty_collection()
        for i, v in self.enumerator(context.value):
            transformed = itypes.validator.transform(context.new(
                value=v,
                keypath_root=concat_keypath(context.keypath_root, i),
                keypath_owner=concat_keypath(context.keypath_owner, i),
                keypath_parent=i,
                parent=context.value,
                fdesc=itypes.fdesc))
            self.append_value(
                self.to_object_key(i, context.config_owner),
                transformed,
                retval)
        return retval

    def tojson(self, context: ToJSONContext) -> Any:
        if context.value is None:
            return None
        if not isinstance(context.value, self.cls):
            return context.value
        itypes = self.item_types(context.config.linked_class)
        retval = self.empty_collection()
        for i, v in self.enumerator(context.value):
            transformed = itypes.validator.tojson(context.new(value=v))
            self.append_value(
                self.to_json_key(i, context.config),
                transformed,
                retval)
        return retval

    def serialize(self, context: TransformingContext) -> Any:
        if context.value is None:
            return None
        if not isinstance(context.value, self.cls):
            return context.value
        itypes = self.item_types(context.config_owner.linked_class)
        retval = self.empty_collection()
        for i, v in self.enumerator(context.value):
            transformed = itypes.validator.serialize(context.new(
                value=v,
                keypath_root=concat_keypath(context.keypath_root, i),
                keypath_owner=concat_keypath(context.keypath_owner, i),
                keypath_parent=i,
                parent=context.value,
                fdesc=itypes.fdesc))
            self.append_value(
                self.to_json_key(i, context.config_owner),
                transformed,
                retval)
        return retval
