"""module for gt modifier."""
from __future__ import annotations
from typing import Callable, Union, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class GtModifier(Modifier):
    """Gt modifier validates value against min value."""

    def __init__(self, gt_value: int | float | Callable | Types):
        self.gt_value = gt_value

    def validate(self, ctx: Ctx) -> None:
        is_number = type(ctx.val) is int or type(ctx.val) is float
        if is_number and ctx.val <= self.resolve_param(self.gt_value, ctx):
            ctx.raise_vexc('value is not greater than '
                           f'{self.gt_value}')
