"""module for max validator."""
from typing import Union
from ..exceptions import ValidationException
from .validator import Validator
from ..ctx import Ctx


class MaxValidator(Validator):
    """Max validator validates value against max value."""

    def __init__(self, max_value: Union[int, float]) -> None:
        self.max_value = max_value

    def validate(self, ctx: Ctx) -> None:
        if ctx.value is None:
            return ctx.value
        if ctx.value > self.max_value:
            raise ValidationException(
                {ctx.keypath_root: f'Value \'{ctx.value}\' at \'{ctx.keypath_root}\' should not be greater than {self.max_value}.'},
                ctx.root
            )
