"""module for padend modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx

class PadEndModifier(Modifier):
    """PadEnd modifier add str to the end of str value.."""

    def __init__(self, char: str, target_length: int) -> None:
        self.char = char
        self.target_length = target_length

    def transform(self, ctx: Ctx) -> Any:
        if type(ctx.val) is str:
            pad_str = (self.target_length - len(ctx.val)) * self.char
            return ctx.val + pad_str
        else:
            return ctx.val
