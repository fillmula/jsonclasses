"""module for neq modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class NeqModifier(Modifier):
    """Neq modifier validates value by unequal testing."""

    def __init__(self, val: Any | Types):
        self.val = val

    def validate(self, ctx: Ctx) -> None:
        from ..types import Types
        if isinstance(self.val, Types):
            against_val = self.val.modifier.transform(ctx)
            if ctx.val == against_val:
                ctx.raise_vexc('value is not unequal')
            else:
                return ctx.val
        elif ctx.val == self.val:
            ctx.raise_vexc('value is not unequal')
        else:
            return ctx.val
