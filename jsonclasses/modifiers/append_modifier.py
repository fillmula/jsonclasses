"""module for append modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING, Any
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class AppendModifier(Modifier):
    """Insert at modifier for adding an element to the end of list"""

    def __init__(self, item: Any) -> None:
        self.item = item

    def transform(self, ctx: Ctx) -> Any:
        if isinstance(ctx.val, list):
            return ctx.val + [self.item]
        elif type(ctx.val) is str:
            return ctx.val + str(self.item)
        else:
            return ctx.val
