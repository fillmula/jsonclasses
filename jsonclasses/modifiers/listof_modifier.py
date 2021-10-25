"""module for listof modifier."""
from __future__ import annotations
from typing import Any, Collection, Iterable, TYPE_CHECKING
from ..fdef import Fdef, FStore, FType, Nullability
from .collection_type_modifier import CollectionTypeModifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class ListOfModifier(CollectionTypeModifier):
    """This modifier validates list."""

    def __init__(self, raw_item_types: Any) -> None:
        super().__init__(raw_item_types)
        self.cls = list
        self.ftype = FType.LIST

    def define(self, fdef: Fdef) -> None:
        super().define(fdef)
        if fdef._fstore == FStore.LOCAL_KEY or fdef._foreign_key is not None:
            if fdef._collection_nullability is Nullability.UNDEFINED:
                fdef._collection_nullability = Nullability.NONNULL

    def enumerator(self, value: list) -> Iterable:
        return enumerate(value)

    def empty_collection(self) -> Collection:
        return []

    def append_value(self, i: int, v: Any, col: list):
        col.append(v)

    def should_special_handle(self, key: Any, v: Any, ctx: Ctx) -> bool:
        is_fkey = ctx.fdef.fstore == FStore.FOREIGN_KEY
        uses_jt = ctx.fdef.use_join_table
        if not (is_fkey and uses_jt):
            return False
        return isinstance(v, dict) and ('_add' in v or '_del' in v)

    def special_handle(self, key: Any, v: Any, ctx: Ctx) -> None:
        fname = ctx.keypatho[-1]
        if '_add' in v:
            ctx.owner._add_link_key(fname, v['_add'])
        elif '_del' in v:
            ctx.owner._add_unlink_key(fname, v['_del'])
