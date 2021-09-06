"""module for max modifier."""
from __future__ import annotations
from typing import Union, TYPE_CHECKING
from ..excs import ValidationException
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class MaxModifier(Modifier):
    """Max modifier validates value against max value."""

    def __init__(self, max_value: Union[int, float]) -> None:
        self.max_value = max_value

    def validate(self, ctx: Ctx) -> None:
        if ctx.val is None:
            return ctx.val
        if ctx.val > self.max_value:
            kp = '.'.join([str(k) for k in ctx.keypathr])
            raise ValidationException(
                {kp: f'value is not less than or equal {self.max_value}'},
                ctx.root
            )
