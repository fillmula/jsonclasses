"""module for length validator."""
from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from ..excs import ValidationException
from .validator import Validator
if TYPE_CHECKING:
    from ..ctx import Ctx


class LengthValidator(Validator):
    """Length validator validate value against the provided length."""

    def __init__(self, minlength: int, maxlength: Optional[int]) -> None:
        self.minlength = minlength
        self.maxlength = maxlength if maxlength is not None else minlength

    def validate(self, ctx: Ctx) -> None:
        if ctx.val is None:
            return
        value = ctx.val
        kp = '.'.join([str(k) for k in ctx.keypathr])
        if len(value) > self.maxlength or len(value) < self.minlength:
            if self.minlength != self.maxlength:
                message = f'Length of value \'{value}\' at \'{kp}\' should not be greater than {self.maxlength} or less than {self.minlength}.'
            else:
                message = f'Length of value \'{value}\' at \'{kp}\' should be {self.minlength}.'
            raise ValidationException(
                {kp: message},
                ctx.root
            )
