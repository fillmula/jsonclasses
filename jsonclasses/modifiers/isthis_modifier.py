"""module for isthis modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx

class IsThisModifier(Modifier):
    """Is this modifier tests value against the context owner."""


    def validate(self, ctx: Ctx) -> None:
        if ctx.val is None:
            ctx.raise_vexc('none is not this')
        if ctx.val is ctx.owner:
            return None
        if ctx.val.__class__ == ctx.owner.__class__:
            if ctx.val._id == ctx.owner._id:
                return None
        ctx.raise_vexc('value is not this')
