"""module for pow modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx

class PowModifier(Modifier):
    """Pow modifier pows number value."""

    def __init__(self, by: int | float):
        self.by = by

    def transform(self, ctx: Ctx) -> Any:
        return pow(self.by, ctx.val) if type(ctx.val) is int or type(ctx.val) is float else ctx.val
