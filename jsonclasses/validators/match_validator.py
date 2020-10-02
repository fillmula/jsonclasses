"""module for match validator."""
from re import search
from ..exceptions import ValidationException
from .validator import Validator
from ..contexts import ValidatingContext


class MatchValidator(Validator):
    """Match validator validates value against pattern."""

    def __init__(self, pattern: str) -> None:
        self.pattern = pattern

    def validate(self, context: ValidatingContext) -> None:
        if context.value is None:
            return
        value = context.value
        if search(self.pattern, value) is None:
            kp = context.keypath_root
            raise ValidationException(
                {kp: f'Value \'{value}\' at \'{kp}\' should match \'{self.pattern}\'.'},
                context.root
            )
