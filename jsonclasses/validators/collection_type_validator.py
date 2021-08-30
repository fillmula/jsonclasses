"""module for listof validator."""
from __future__ import annotations
from typing import (
    Any, Collection, Iterable, TypeVar, Union, TYPE_CHECKING
)
from ..fdef import Fdef, Nullability
from ..jconf import JConf
from ..excs import ValidationException
from .type_validator import TypeValidator
if TYPE_CHECKING:
    from ..jobject import JObject
    from ..types import Types
    from ..ctx import Ctx


T = TypeVar('T', bound=Collection)


class CollectionTypeValidator(TypeValidator):
    """Base class for collection type validators."""

    def __init__(self, raw_item_types: Any) -> None:
        super().__init__()
        self.raw_item_types = raw_item_types
        self.exact_type = False

    def define(self, fdef: Fdef) -> None:
        super().define(fdef)
        fdef._raw_item_types = self.raw_item_types

    def enumerator(self, value: Collection) -> Iterable:
        raise NotImplementedError('please implement enumerator')

    def empty_collection(self) -> Collection:
        raise NotImplementedError('please override empty_collection')

    def append_value(self, i: Union[str, int], v: Any, col: Collection):
        raise NotImplementedError('please implement append_value')

    def to_object_key(self, key: T, conf: JConf) -> T:
        return key

    def to_json_key(self, key: T, conf: JConf) -> T:
        return key

    def validate(self, ctx: Ctx) -> None:
        if ctx.val is None:
            return
        super().validate(ctx)
        itypes = ctx.fdef.item_types
        all_fields = next(b for b in [
            ctx.ctxcfg.all_fields,
            ctx.cdefowner.jconf.validate_all_fields] if b is not None)
        keypath_messages = {}
        for i, v in self.enumerator(ctx.val):
            try:
                ictx = ctx.colval(v, i, itypes.fdef, ctx.val)
                itypes.validator.validate(ictx)
            except ValidationException as exception:
                if all_fields:
                    keypath_messages.update(exception.keypath_messages)
                else:
                    raise exception
        if len(keypath_messages) > 0:
            raise ValidationException(
                keypath_messages=keypath_messages,
                root=ctx.root)

    def transform(self, ctx: Ctx) -> Any:
        if ctx.val is None:
            if ctx.fdef.collection_nullability == Nullability.NONNULL:
                return self.empty_collection()
            else:
                return None
        if not isinstance(ctx.val, self.cls):
            return ctx.val
        itypes = ctx.fdef.item_types
        retval = self.empty_collection()
        for i, v in self.enumerator(ctx.val):
            ictx = ctx.colval(v, i, itypes.fdef, ctx.val)
            tsfmd = itypes.validator.transform(ictx)
            self.append_value(
                self.to_object_key(i, ctx.owner.cdef.jconf), tsfmd, retval)
        return retval

    def tojson(self, ctx: Ctx) -> Any:
        if ctx.val is None:
            return None
        if not isinstance(ctx.val, self.cls):
            return ctx.val
        itypes = ctx.fdef.item_types
        retval = self.empty_collection()
        for i, v in self.enumerator(ctx.val):
            ictx = ctx.colval(v, i, itypes.fdef, ctx.val)
            tsfmd = itypes.validator.tojson(ictx)
            self.append_value(
                    self.to_json_key(i, ctx.owner.cdef.jconf), tsfmd, retval)
        return retval

    def serialize(self, ctx: Ctx) -> Any:
        if ctx.val is None:
            return None
        if not isinstance(ctx.val, self.cls):
            return ctx.val
        itypes = ctx.fdef.item_types
        retval = self.empty_collection()
        for i, v in self.enumerator(ctx.val):
            ictx = ctx.colval(v, i, itypes.fdef, ctx.val)
            tsfmd = itypes.validator.serialize(ictx)
            self.append_value(
                    self.to_json_key(i, ctx.cdefowner.jconf), tsfmd, retval)
        return retval
