"""module for length validator."""
from typing import Optional
from ..exceptions import ValidationException
from .validator import Validator
from ..contexts import ValidatingContext


class LengthValidator(Validator):
    """Length validator validate value against the provided length."""

    def __init__(self, minlength: int, maxlength: Optional[int]) -> None:
        self.minlength = minlength
        self.maxlength = maxlength if maxlength is not None else minlength

    def validate(self, context: ValidatingContext) -> None:
        if context.value is None:
            return
        value = context.value
        kp = context.keypath_root
        if len(value) > self.maxlength or len(value) < self.minlength:
            if self.minlength != self.maxlength:
                message = f'Length of value \'{value}\' at \'{kp}\' should not be greater than {self.maxlength} or less than {self.minlength}.'
            else:
                message = f'Length of value \'{value}\' at \'{kp}\' should be {self.minlength}.'
            raise ValidationException(
                {kp: message},
                context.root
            )
