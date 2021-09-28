"""module for split modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx

class SplitModifier(Modifier):
    """Split modifier split value."""

    def __init__(self, sep: str) -> None:
        self.sep = sep

    def transform(self, ctx: Ctx) -> Any:
        is_str = type(ctx.val) is str
        return ctx.val.split(self.sep) if is_str else ctx.val
