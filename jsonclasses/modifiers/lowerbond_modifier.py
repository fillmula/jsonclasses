"""module for lowerbond modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING, Callable
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types

class LowerbondModifier(Modifier):
    """Lowerbond modifier returns the value of the field to lowerbond if
    the value of the field is smaller than lowerbond."""

    def __init__(self, min_value: int | float | Callable | Types) -> None:
        self.min_value = min_value

    def transform(self, ctx: Ctx) -> Any:
        min_value = self.resolve_param(self.min_value, ctx)
        if type(ctx.val) is int or type(ctx.val) is float:
            if ctx.val < min_value:
                return min_value
            else:
                return ctx.val
        else:
            return ctx.val
