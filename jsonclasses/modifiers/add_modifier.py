"""module for add modifier."""
from __future__ import annotations
from typing import Any, Union, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx

class AddModifier(Modifier):
    """Add modifier adds number value."""

    def __init__(self, by: int | float):
        self.by = by

    def transform(self, ctx: Ctx) -> Any:
        return self.by + ctx.val if type(ctx.val) is int or type(ctx.val) is float else ctx.val
