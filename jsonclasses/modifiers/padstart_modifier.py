"""module for padstart modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx

class PadStartModifier(Modifier):
    """PadStart modifier add str to the start of str value."""

    def __init__(self, char: str, target_length: int) -> None:
        self.char = char
        self.target_length = target_length

    def transform(self, ctx: Ctx) -> Any:
        if type(ctx.val) is str:
            pad_str = (self.target_length - len(ctx.val)) * self.char
            return pad_str + ctx.val
        else:
            return ctx.val
