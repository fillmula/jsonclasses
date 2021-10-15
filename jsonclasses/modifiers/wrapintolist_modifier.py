"""module for wrap into list modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING, Any
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class WrapIntoListModifier(Modifier):
    """Wrap value into a list."""

    def transform(self, ctx: Ctx) -> Any:
        return None if ctx.val is None else [ctx.val]
