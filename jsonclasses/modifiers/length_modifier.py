"""module for length modifier."""
from __future__ import annotations
from typing import Callable, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class LengthModifier(Modifier):
    """Length modifier validate value against the provided length."""

    def __init__(self, minlength: int | Callable | Types, maxlength: int | Callable | Types | None = None) -> None:
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
