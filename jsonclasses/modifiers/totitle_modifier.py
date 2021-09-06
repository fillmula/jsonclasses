"""module for totitle modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class ToTitleModifier(Modifier):
    """Convert string to title format."""

    def transform(self, ctx: Ctx) -> Any:
        return None if ctx.val is None else ctx.val.title()

