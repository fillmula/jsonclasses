"""module for min validator."""
from __future__ import annotations
from typing import Union, TYPE_CHECKING
from ..excs import ValidationException
from .validator import Validator
if TYPE_CHECKING:
    from ..ctx import Ctx


class MinValidator(Validator):
    """Min validator validates value against min value."""

    def __init__(self, min_value: Union[int, float]):
        self.min_value = min_value

    def validate(self, ctx: Ctx) -> None:
        if ctx.val is None:
            return
        if ctx.val < self.min_value:
            kp = '.'.join([str(k) for k in ctx.keypathr])
            raise ValidationException(
                {kp: f'Value \'{ctx.val}\' at \'{kp}\' should not be less than {self.min_value}.'},
                ctx.root
            )
