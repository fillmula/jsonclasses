"""module for negative validator."""
from __future__ import annotations
from typing import TYPE_CHECKING
from ..exceptions import ValidationException
from .validator import Validator
if TYPE_CHECKING:
    from ..ctx import Ctx


class NegativeValidator(Validator):
    """Negative validator marks value valid for smaller than zero."""

    def validate(self, ctx: Ctx) -> None:
        if ctx.value is None:
            return ctx.value
        if ctx.value >= 0:
            kp = '.'.join([str(k) for k in ctx.keypathr])
            v = ctx.value
            raise ValidationException(
                {kp: f'Value \'{v}\' at \'{kp}\' should be negative.'},
                ctx.root
            )
