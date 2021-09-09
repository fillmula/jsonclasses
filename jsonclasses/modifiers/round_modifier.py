"""module for round modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx

class RoundModifier(Modifier):
    """Round modifier rounds number value."""

    def transform(self, ctx: Ctx) -> Any:
        is_number = type(ctx.val) is int or type(ctx.val) is float
        return round(ctx.val) if is_number else ctx.val
