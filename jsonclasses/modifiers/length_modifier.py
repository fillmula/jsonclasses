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
        if ctx.val is None:
            return
        value = ctx.val
        if len(value) > self.maxlength or len(value) < self.minlength:
            if self.minlength != self.maxlength:
                message = f'length of value should be in between {self.minlength} and {self.maxlength}'
            else:
                message = f'length of value is not {self.minlength}'
            ctx.raise_vexc(message)
