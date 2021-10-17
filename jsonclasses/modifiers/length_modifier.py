"""module for length modifier."""
from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from ..excs import ValidationException
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class LengthModifier(Modifier):
    """Length modifier validate value against the provided length."""

    def __init__(self, minlength: int, maxlength: Optional[int]) -> None:
        self.minlength = minlength
        self.maxlength = maxlength if maxlength is not None else minlength

    def validate(self, ctx: Ctx) -> None:
        if isinstance(ctx.val, list) or type(ctx.val) is str:
            minlength = self.resolve_param(self.minlength, ctx)
            if self.minlength == self.maxlength:
                maxlength = minlength
            else:
                maxlength = self.resolve_param(self.maxlength, ctx)
            if len(ctx.val) > maxlength or len(ctx.val) < minlength:
                if minlength != maxlength:
                    msg = f'length of value is not between {minlength} and {maxlength}'
                else:
                    msg = f'length of value is not {minlength}'
                ctx.raise_vexc(msg)
        return ctx.val
