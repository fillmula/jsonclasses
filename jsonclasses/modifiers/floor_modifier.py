"""module for floor modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from math import floor
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx

class FloorModifier(Modifier):
    """Floor modifier Floor number value."""

    def transform(self, ctx: Ctx) -> Any:
        is_number = type(ctx.val) is int or type(ctx.val) is float
        return floor(ctx.val) if is_number else ctx.val
