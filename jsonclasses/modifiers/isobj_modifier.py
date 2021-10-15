"""module for isobj modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..jobject import JObject
    from ..types import Types

class IsObjModifier(Modifier):
    """Check if value is the same with provided object."""

    def __init__(self, getter: Types) -> None:
        self.getter = getter

    def validate(self, ctx: Ctx) -> None:
        if ctx.val is None:
            ctx.raise_vexc('none is not an object')
        transformed = self.getter.modifier.transform(ctx)
        if transformed is None:
            ctx.raise_vexc('comparing value not found')
        if transformed.__class__.__name__ == ctx.val.__class__.__name__:
            if transformed._id == ctx.val._id:
                return
        ctx.raise_vexc('objects are not equal')
        # future add ObjRef here and also fval
