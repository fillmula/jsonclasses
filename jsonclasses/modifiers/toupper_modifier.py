"""module for toupper modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class ToUpperModifier(Modifier):
    """Convert string into uppercase."""

    def transform(self, ctx: Ctx) -> Any:
        return ctx.val.upper() if isinstance(ctx.val, str) else ctx.val
