"""module for lt modifier."""
from __future__ import annotations
from typing import Union, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class LtModifier(Modifier):
    """Lt modifier validates value aganinst max value."""

    def __init__(self, lt_value: Union[int, float]) -> None:
        self.lt_value = lt_value

    def validate(self, ctx: Ctx) -> None:
        is_number = type(ctx.val) is int or type(ctx.val) is float
        if is_number and ctx.val >= self.lt_value:
            ctx.raise_vexc(f'value is not less than {self.lt_value}')
