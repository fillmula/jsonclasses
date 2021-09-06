"""module for positive modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING
from ..excs import ValidationException
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class PositiveModifier(Modifier):
    """Positive modifier marks value valid for large than zero."""

    def validate(self, ctx: Ctx) -> None:
        if ctx.val is None:
            return ctx.val
        if ctx.val <= 0:
            kp = '.'.join([str(k) for k in ctx.keypathr])
            v = ctx.val
            raise ValidationException(
                {kp: f'value is not positive'},
                ctx.root
            )
