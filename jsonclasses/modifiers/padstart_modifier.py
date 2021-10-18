"""module for padstart modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING, Callable
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types

class PadStartModifier(Modifier):
    """PadStart modifier add str to the start of str value."""

    def __init__(self, char: str | Callable | Types, target_length: int | Callable | Types) -> None:
        self.char = char
        self.target_length = target_length

    def transform(self, ctx: Ctx) -> Any:
        char = self.resolve_param(self.char, ctx)
        target_length = self.resolve_param(self.target_length, ctx)
        if type(ctx.val) is str:
            pad_str = (target_length - len(ctx.val)) * char
            return pad_str + ctx.val
        else:
            return ctx.val
