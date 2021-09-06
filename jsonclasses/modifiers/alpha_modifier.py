"""module for alpha modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class AlphaModifier(Modifier):
    """Alpha modifier raises if value is not alpha string."""

    def validate(self, ctx: Ctx) -> None:
        if isinstance(ctx.val, str) and not ctx.val.isalpha():
            ctx.raise_vexc('value is not alpha str')
