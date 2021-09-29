"""module for tofloat modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class ToFloatModifier(Modifier):
    """ToFloat Modifier transforms value into a float"""

    def transform(self, ctx: Ctx) -> Any:
        is_str_or_bool = type(ctx.val) is bool or type(ctx.val) is str
        return float(ctx.val) if is_str_or_bool else ctx.val
