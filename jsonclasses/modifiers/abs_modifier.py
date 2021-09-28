"""module for abs modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx

class AbsModifier(Modifier):
    """Abs modifier transforms number value to its absolute value."""

    def transform(self, ctx: Ctx) -> Any:
        is_number = type(ctx.val) is int or type(ctx.val) is float
        return abs(ctx.val) if is_number else ctx.val
