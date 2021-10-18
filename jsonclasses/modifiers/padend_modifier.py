"""module for padend modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING, Callable
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types

class PadEndModifier(Modifier):
    """PadEnd modifier add str to the end of str value.."""

    def __init__(self, char: str | Callable | Types, target_length: int | Callable | Types) -> None:
        self.char = char
        self.target_length = target_length

    def transform(self, ctx: Ctx) -> Any:
        target_length = self.resolve_param(self.target_length, ctx)
        char = self.resolve_param(self.char, ctx)
        if type(ctx.val) is str:
            pad_str = (target_length - len(ctx.val)) * char
            return ctx.val + pad_str
        else:
            return ctx.val
