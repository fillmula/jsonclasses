"""module for replace modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING, Callable
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types

class ReplaceModifier(Modifier):
    """Replace modifier Replace  value."""

    def __init__(self, old: str | Callable | Types, new: str | Callable | Types) -> None:
        self.old = old
        self.new = new

    def transform(self, ctx: Ctx) -> Any:
        is_str = type(ctx.val) is str
        old = self.resolve_param(self.old, ctx)
        new = self.resolve_param(self.new, ctx)
        return ctx.val.replace(old, new) if is_str else ctx.val
