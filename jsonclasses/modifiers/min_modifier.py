"""module for min modifier."""
from __future__ import annotations
from typing import Union, TYPE_CHECKING
from ..excs import ValidationException
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class MinModifier(Modifier):
    """Min modifier validates value against min value."""

    def __init__(self, min_value: Union[int, float]):
        self.min_value = min_value

    def validate(self, ctx: Ctx) -> None:
        is_number = type(ctx.val) is int or type(ctx.val) is float
        if is_number and ctx.val < self.min_value:
            ctx.raise_vexc('value is not greater than or equal '
                           f'{self.min_value}')
