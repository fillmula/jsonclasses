"""module for lt modifier."""
from __future__ import annotations
from typing import Callable, Union, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class LtModifier(Modifier):
    """Lt modifier validates value aganinst max value."""

    def __init__(self, lt_value: int | float | Callable | Types):
        self.lt_value = lt_value

    def validate(self, ctx: Ctx) -> None:
        is_number = type(ctx.val) is int or type(ctx.val) is float
        if is_number and ctx.val >= self.resolve_param(self.lt_value, ctx):
            ctx.raise_vexc(f'value is not less than {self.resolve_param(self.lt_value, ctx)}')
