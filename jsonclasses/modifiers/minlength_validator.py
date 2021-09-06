"""module for minlength modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING
from ..excs import ValidationException
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class MinlengthModifier(Modifier):
    """Minlength modifier validates value against min length."""

    def __init__(self, minlength: int) -> None:
        self.minlength = minlength

    def validate(self, ctx: Ctx) -> None:
        if ctx.val is None:
            return
        if len(ctx.val) < self.minlength:
            kp = '.'.join([str(k) for k in ctx.keypathr])
            raise ValidationException(
                {kp: f'length of value is not greater than or equal {self.minlength}'},
                ctx.root
            )
