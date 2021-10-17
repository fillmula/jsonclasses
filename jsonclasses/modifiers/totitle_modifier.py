"""module for totitle modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class ToTitleModifier(Modifier):
    """Convert string into title format."""

    def transform(self, ctx: Ctx) -> Any:
        return ctx.val.title() if isinstance(ctx.val, str) else ctx.val
