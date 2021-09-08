"""module for max modifier."""
from __future__ import annotations
from typing import Union, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class MaxModifier(Modifier):
    """Max modifier validates value against max value."""

    def __init__(self, max_value: Union[int, float]) -> None:
        self.max_value = max_value

    def validate(self, ctx: Ctx) -> None:
        is_number = type(ctx.val) is int or type(ctx.val) is float
        if is_number and ctx.val > self.max_value:
            ctx.raise_vexc(f'value is not less than or equal {self.max_value}')
