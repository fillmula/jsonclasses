"""module for max validator."""
from typing import Union
from ..exceptions import ValidationException
from .validator import Validator
from ..contexts import ValidatingContext


class MaxValidator(Validator):
    """Max validator validates value against max value."""

    def __init__(self, max_value: Union[int, float]) -> None:
        self.max_value = max_value

    def validate(self, context: ValidatingContext) -> None:
        if context.value is None:
            return context.value
        if context.value > self.max_value:
            raise ValidationException(
                {context.keypath_root: f'Value \'{context.value}\' at \'{context.keypath_root}\' should not be greater than {self.max_value}.'},
                context.root
            )
