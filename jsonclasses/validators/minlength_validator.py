"""module for minlength validator."""
from ..exceptions import ValidationException
from .validator import Validator
from ..ctx import Ctx


class MinlengthValidator(Validator):
    """Minlength validator validates value against min length."""

    def __init__(self, minlength: int) -> None:
        self.minlength = minlength

    def validate(self, ctx: Ctx) -> None:
        if ctx.value is None:
            return
        if len(ctx.value) < self.minlength:
            raise ValidationException(
                {ctx.keypath_root: f'Length of value \'{ctx.value}\' at \'{ctx.keypath_root}\' should not be less than {self.minlength}.'},
                ctx.root
            )
