"""module for isobj modifier."""
from __future__ import annotations
from typing import cast, TYPE_CHECKING
from ..objref import ObjRef
from ..isjsonclass import isjsonobject
from ..jobject import JObject
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
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
        this = cast(JObject | ObjRef, ctx.val)
        that = cast(JObject | ObjRef, transformed)
        if isjsonobject(this):
            this_cls = this.__class__.__name__
            this_id = this._id
        else:
            this_cls = this.cls
            this_id = this.id
        if isjsonobject(that):
            that_cls = that.__class__.__name__
            that_id = that._id
        else:
            that_cls = that.cls
            that_id = that.id
        if that_cls == this_cls and that_id == this_id:
            return
        ctx.raise_vexc('objects are not equal')
