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
        if ctx.val is None:
            return
        if ctx.val < self.min_value:
            kp = '.'.join([str(k) for k in ctx.keypathr])
            raise ValidationException(
                {kp: f'value is not greater than or equal {self.min_value}'},
                ctx.root
            )
