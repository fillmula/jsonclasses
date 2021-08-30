"""module for maxlength validator."""
from __future__ import annotations
from typing import TYPE_CHECKING
from ..excs import ValidationException
from .validator import Validator
if TYPE_CHECKING:
    from ..ctx import Ctx


class MaxlengthValidator(Validator):
    """Maxlength validator validates value against max length."""

    def __init__(self, maxlength: int) -> None:
        self.maxlength = maxlength

    def validate(self, ctx: Ctx) -> None:
        if ctx.val is None:
            return
        if len(ctx.val) > self.maxlength:
            kp = '.'.join([str(k) for k in ctx.keypathr])
            raise ValidationException(
                {kp: f'Length of value \'{ctx.val}\' at \'{kp}\' should not be greater than {self.maxlength}.'},
                ctx.root
            )
