"""module for sqrt modifier."""
from __future__ import annotations
from math import sqrt
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx

class SqrtModifier(Modifier):
    """Sqrt modifier sqrts number value."""

    def transform(self, ctx: Ctx) -> Any:
        if type(ctx.val) is int or type(ctx.val) is float:
            if(ctx.val >= 0):
                return sqrt(ctx.val)
            else:
                ctx.raise_vexc('value is less than 0 thus cannot be sqrted')
        else:
            return ctx.val
