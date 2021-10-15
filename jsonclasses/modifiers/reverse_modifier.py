"""module for reverse modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx

class ReverseModifier(Modifier):
    """Reverse modifier reverses iterable values."""

    def transform(self, ctx: Ctx) -> Any:
        is_iterable = type(ctx.val) is str or isinstance(ctx.val, list)
        return ctx.val[::-1] if is_iterable else ctx.val
