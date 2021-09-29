"""module for tolist modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class ToListModifier(Modifier):
    """ToList Modifier transforms value into a list"""

    def transform(self, ctx: Ctx) -> Any:
        is_set_or_str_or_tuple = type(ctx.val) is set or type(ctx.val) is str or type(ctx.val) is tuple
        return list(ctx.val) if is_set_or_str_or_tuple else ctx.val
