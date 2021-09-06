"""module for maxlength modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING
from ..excs import ValidationException
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class MaxlengthModifier(Modifier):
    """Maxlength modifier validates value against max length."""

    def __init__(self, maxlength: int) -> None:
        self.maxlength = maxlength

    def validate(self, ctx: Ctx) -> None:
        if ctx.val is None:
            return
        if len(ctx.val) > self.maxlength:
            ctx.raise_vexc('length of value is not less than or equal '
                           f'{self.maxlength}')
