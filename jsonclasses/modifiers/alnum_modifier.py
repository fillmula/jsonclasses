"""module for alnum modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class AlnumModifier(Modifier):
    """Alnum modifier raises if value is not alnum string."""

    def validate(self, ctx: Ctx) -> None:
        if isinstance(ctx.val, str) and not ctx.val.isalnum():
            ctx.raise_vexc('value is not alnum str')
