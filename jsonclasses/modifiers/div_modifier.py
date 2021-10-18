"""module for div modifier."""
from __future__ import annotations
from typing import Any, Callable, Union, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types

class DivModifier(Modifier):
    """Div modifier divs number value."""

    def __init__(self, by: int | float | Callable | Types):
        self.by = by

    def transform(self, ctx: Ctx) -> Any:
        return ctx.val / self.resolve_param(self.by, ctx) if type(ctx.val) is int or type(ctx.val) is float else ctx.val
