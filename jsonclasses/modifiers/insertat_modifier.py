"""module for insert at modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING, Any
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class InsertAtModifier(Modifier):
    """Insert at modifier for inserting an element to the list"""

    def __init__(self, item: Any, index: int) -> None:
        self.item = item
        self.index = index

    def transform(self, ctx: Ctx) -> Any:
        if isinstance(ctx.val, list):
            return ctx.val[:self.index] + [self.item] + ctx.val[self.index:]
        elif type(ctx.val) is str:
            return ctx.val[:self.index] + str(self.item) + ctx.val[self.index:]
        else:
            return ctx.val
