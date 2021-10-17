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
        if isinstance(ctx.val, list) or type(ctx.val) is str:
            if len(ctx.val) > self.resolve_param(self.maxlength, ctx):
                ctx.raise_vexc('length of value is not less than or equal '
                            f'{self.maxlength}')
        return ctx.val
