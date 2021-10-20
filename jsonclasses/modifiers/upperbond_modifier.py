"""module for upperbond modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING, Callable
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types

class UpperBondModifier(Modifier):
    """Upper bond modifier returns the value of the field to upperbond if
    the value of the field is larger than upperbond."""

    def __init__(self, is_number: int | float | Callable | Types) -> None:
        self.is_number = is_number

    def transform(self, ctx: Ctx) -> Any:
        if ctx.val is None:
            return None
        if type(ctx.val) is int or type(ctx.val) is float:
            if self.resolve_param(self.is_number, ctx) > ctx.val:
                return ctx.val
            else:
                return self.resolve_param(self.is_number, ctx)
        else:
            return ctx.val
