"""module for gt modifier."""
from __future__ import annotations
from typing import Union, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class GtModifier(Modifier):
    """Gt modifier validates value against min value."""

    def __init__(self, gt_value: Union[int, float]):
        self.gt_value = gt_value

    def validate(self, ctx: Ctx) -> None:
        is_number = type(ctx.val) is int or type(ctx.val) is float
        if is_number and ctx.val <= self.gt_value:
            ctx.raise_vexc('value is not greater than '
                           f'{self.gt_value}')
