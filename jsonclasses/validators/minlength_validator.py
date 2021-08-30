"""module for minlength validator."""
from __future__ import annotations
from typing import TYPE_CHECKING
from ..excs import ValidationException
from .validator import Validator
if TYPE_CHECKING:
    from ..ctx import Ctx


class MinlengthValidator(Validator):
    """Minlength validator validates value against min length."""

    def __init__(self, minlength: int) -> None:
        self.minlength = minlength

    def validate(self, ctx: Ctx) -> None:
        if ctx.val is None:
            return
        if len(ctx.val) < self.minlength:
            kp = '.'.join([str(k) for k in ctx.keypathr])
            raise ValidationException(
                {kp: f'Length of value \'{ctx.val}\' at \'{kp}\' should not be less than {self.minlength}.'},
                ctx.root
            )
