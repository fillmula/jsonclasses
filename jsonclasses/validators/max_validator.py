"""module for max validator."""
from __future__ import annotations
from typing import Union, TYPE_CHECKING
from ..exceptions import ValidationException
from .validator import Validator
if TYPE_CHECKING:
    from ..ctx import Ctx


class MaxValidator(Validator):
    """Max validator validates value against max value."""

    def __init__(self, max_value: Union[int, float]) -> None:
        self.max_value = max_value

    def validate(self, ctx: Ctx) -> None:
        if ctx.value is None:
            return ctx.value
        if ctx.value > self.max_value:
            kp = '.'.join([str(k) for k in ctx.keypathr])
            raise ValidationException(
                {kp: f'Value \'{ctx.value}\' at \'{kp}\' should not be greater than {self.max_value}.'},
                ctx.root
            )
