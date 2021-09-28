"""module for replace modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx

class ReplaceModifier(Modifier):
    """Replace modifier Replace  value."""

    def __init__(self, old: str, new: str) -> None:
        self.old = old
        self.new = new

    def transform(self, ctx: Ctx) -> Any:
        is_str = type(ctx.val) is str
        return ctx.val.replace(self.old, self.new) if is_str else ctx.val

