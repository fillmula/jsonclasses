"""module for oneof validator."""
from ..exceptions import ValidationException
from .validator import Validator
from ..contexts import ValidatingContext


class OneOfValidator(Validator):
    """One of validator validates value against a list of available values."""

    def __init__(self, str_list: list[str]) -> None:
        self.str_list = str_list

    def validate(self, context: ValidatingContext) -> None:
        if context.value is None:
            return None
        if context.value not in self.str_list:
            raise ValidationException(
                {context.keypath_root: f'Value \'{context.value}\' at \'{context.keypath_root}\' should be one of {self.str_list}.'},
                context.root
            )
