"""module for upperbond modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING, Callable
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types

class UpperbondModifier(Modifier):
    """Upperbond modifier returns the value of the field to upperbond if
    the value of the field is larger than upperbond."""

    def __init__(self, max_value: int | float | Callable | Types) -> None:
        self.max_value = max_value

    def transform(self, ctx: Ctx) -> Any:
        if ctx.val is None:
            return None
        if type(ctx.val) is int or type(ctx.val) is float:
            if ctx.val > self.resolve_param(self.max_value, ctx):
                return self.resolve_param(self.max_value, ctx)
            else:
                return ctx.val
        else:
            return ctx.val
