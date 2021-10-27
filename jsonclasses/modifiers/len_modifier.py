"""module for len modifier."""
from __future__ import annotations
from typing import Callable, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class LenModifier(Modifier):
    """Len modifier return the length of value."""

    def transform(self, ctx: Ctx) -> int:
        is_str_or_list = isinstance(ctx.val, list) or type(ctx.val) is str
        return len(ctx.val) if is_str_or_list else ctx.val
