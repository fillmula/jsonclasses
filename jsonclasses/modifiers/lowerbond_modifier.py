"""module for lowerbond modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING, Callable
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types

class LowerBondModifier(Modifier):
    """Lower bond modifier returns the value of the field to lowerbond if
    the value of the field is smaller than lowerbond."""

    def __init__(self, is_number: int | float | Callable | Types) -> None:
        self.is_number = is_number

    def transform(self, ctx: Ctx) -> Any:
        if ctx.val is None:
            return None
        if type(ctx.val) is int or type(ctx.val) is float:
            if self.resolve_param(self.is_number, ctx) < ctx.val:
                return ctx.val
            else:
                return self.resolve_param(self.is_number, ctx)
        else:
            return ctx.val
