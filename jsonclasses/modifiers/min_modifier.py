"""module for min modifier."""
from __future__ import annotations
from typing import Callable, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class MinModifier(Modifier):
    """Min modifier validates value against min value."""

    def __init__(self, min_value: int | float | Callable | Types):
        self.min_value = min_value

    def validate(self, ctx: Ctx) -> None:
        is_number = type(ctx.val) is int or type(ctx.val) is float
        if is_number and ctx.val < self.resolve_param(self.min_value, ctx):
            ctx.raise_vexc('value is not greater than or equal '
                           f'{self.resolve_param(self.min_value, ctx)}')
