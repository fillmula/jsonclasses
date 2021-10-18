"""module for max modifier."""
from __future__ import annotations
from typing import Callable, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class MaxModifier(Modifier):
    """Max modifier validates value against max value."""

    def __init__(self, max_value: int | float | Callable | Types) -> None:
        self.max_value = max_value

    def validate(self, ctx: Ctx) -> None:
        is_number = type(ctx.val) is int or type(ctx.val) is float
        if is_number and ctx.val > self.resolve_param(self.max_value, ctx):
            ctx.raise_vexc(f'value is not less than or equal {self.resolve_param(self.max_value, ctx)}')
