"""module for mongoid modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
from ..fdef import FDef, FSubtype
if TYPE_CHECKING:
    from ..ctx import Ctx


class MongoIdModifier(Modifier):
    """Marks a field as mongoid and set the default value."""

    def define(self, fdef: FDef) -> None:
        fdef._fsubtype = FSubtype.MONGOID

    def transform(self, ctx: Ctx) -> Any:
        from bson.objectid import ObjectId
        return str(ObjectId()) if ctx.val is None else ctx.val
