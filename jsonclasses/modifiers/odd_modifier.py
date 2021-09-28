"""module for odd modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class OddModifier(Modifier):
    """Odd modifier raises if int value is not odd."""

    def validate(self, ctx: Ctx) -> None:
        if type(ctx.val) is int and ctx.val % 2 == 0:
            ctx.raise_vexc('value is not odd')
