"""module for min validator."""
from __future__ import annotations
from typing import Union, TYPE_CHECKING
from ..exceptions import ValidationException
from .validator import Validator
if TYPE_CHECKING:
    from ..ctx import Ctx


class MinValidator(Validator):
    """Min validator validates value against min value."""

    def __init__(self, min_value: Union[int, float]):
        self.min_value = min_value

    def validate(self, ctx: Ctx) -> None:
        if ctx.value is None:
            return
        if ctx.value < self.min_value:
            kp = '.'.join([str(k) for k in ctx.keypathr])
            raise ValidationException(
                {kp: f'Value \'{ctx.value}\' at \'{kp}\' should not be less than {self.min_value}.'},
                ctx.root
            )
