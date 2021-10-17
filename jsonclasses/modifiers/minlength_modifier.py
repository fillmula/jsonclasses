"""module for minlength modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING, Callable
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class MinlengthModifier(Modifier):
    """Minlength modifier validates value against min length."""

    def __init__(self, minlength: int | Callable | Types) -> None:
        self.minlength = minlength

    def validate(self, ctx: Ctx) -> None:
        if isinstance(ctx.val, list) or type(ctx.val) is str:
            if len(ctx.val) < self.resolve_param(self.minlength, ctx):
                ctx.raise_vexc('length of value is not greater than or equal '
                            f'{self.minlength}')
        return ctx.val
