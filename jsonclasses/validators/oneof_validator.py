"""module for oneof validator."""
from ..exceptions import ValidationException
from .validator import Validator
from ..ctx import Ctx


class OneOfValidator(Validator):
    """One of validator validates value against a list of available values."""

    def __init__(self, str_list: list[str]) -> None:
        self.str_list = str_list

    def validate(self, ctx: Ctx) -> None:
        if ctx.value is None:
            return None
        if ctx.value not in self.str_list:
            raise ValidationException(
                {ctx.keypath_root: f'Value \'{ctx.value}\' at \'{ctx.keypath_root}\' should be one of {self.str_list}.'},
                ctx.root
            )
