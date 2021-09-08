"""module for negative modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class NegativeModifier(Modifier):
    """Negative modifier marks value valid for smaller than zero."""

    def validate(self, ctx: Ctx) -> None:
        is_number = type(ctx.val) is int or type(ctx.val) is float
        if is_number and ctx.val >= 0:
            ctx.raise_vexc('value is not negative')
