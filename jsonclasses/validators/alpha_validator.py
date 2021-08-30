"""module for alpha validator."""
from __future__ import annotations
from typing import TYPE_CHECKING
from ..excs import ValidationException
from .validator import Validator
if TYPE_CHECKING:
    from ..ctx import Ctx


class AlphaValidator(Validator):
    """Alpha validator raises if value is not a alpha."""

    def validate(self, ctx: Ctx) -> None:
        if ctx.val is None:
            return
        value = ctx.val
        if not value.isalpha():
            kp = '.'.join([str(k) for k in ctx.keypathr])
            raise ValidationException(
                {kp: f'product_name \'{value}\' at \'{kp}\' is not a alpha.'},
                ctx.root
            )
