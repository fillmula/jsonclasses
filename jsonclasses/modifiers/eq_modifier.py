"""module for eq modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING, Callable
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class EqModifier(Modifier):
    """Eq modifier validates value by equal testing."""

    def __init__(self, val: Any | Types | Callable):
        self.val = val

    def validate(self, ctx: Ctx) -> None:
        from ..types import Types
        # if isinstance(self.val, Types):
        #     against_val = self.val.modifier.transform(ctx)
        #     if ctx.val != against_val:
        #         ctx.raise_vexc('value is not equal')
        #     else:
        #         return ctx.val
        # elif ctx.val != self.val:
        #     ctx.raise_vexc('value is not equal')
        # else:
        #     return ctx.val
        if ctx.val != self.resolve_param(self.val):
            ctx.raise_vexc('value is not equal')
        else:
            return ctx.val
