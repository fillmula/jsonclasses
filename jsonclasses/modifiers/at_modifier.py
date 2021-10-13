"""module for at modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx

class AtModifier(Modifier):
    """At modifier returns result with subscription index."""

    def __init__(self, index: Any) -> None:
        self.index = index

    def transform(self, ctx: Ctx) -> Any:
        if ctx.val is None:
            return None
        return ctx.val[self.index]
