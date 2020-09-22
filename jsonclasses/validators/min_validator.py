"""module for min validator."""
from typing import Union
from ..exceptions import ValidationException
from .validator import Validator
from ..contexts import ValidatingContext


class MinValidator(Validator):
    """Match validator validates value against min value."""

    def __init__(self, min_value: Union[int, float]):
        self.min_value = min_value

    def validate(self, context: ValidatingContext) -> None:
        if context.value is None:
            return
        if context.value < self.min_value:
            raise ValidationException(
                {context.keypath: f'Value \'{context.value}\' at \'{context.keypath}\' should not be less than {self.min_value}.'},
                context.root
            )
