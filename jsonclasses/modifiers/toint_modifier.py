"""module for toint modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class ToIntModifier(Modifier):
    """ToInt Modifier transforms value into a int"""

    def transform(self, ctx: Ctx) -> Any:
        is_str_or_bool = type(ctx.val) is bool or type(ctx.val) is str
        return int(ctx.val) if is_str_or_bool else ctx.val
