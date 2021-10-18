"""module for insert at modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class InsertAtModifier(Modifier):
    """Insert at modifier for inserting an element to the list"""

    def __init__(self, item: Any | Callable | Types, index: int | Callable | Types) -> None:
        self.item = item
        self.index = index

    def transform(self, ctx: Ctx) -> Any:
        index = self.resolve_param(self.index, ctx)
        item = self.resolve_param(self.item, ctx)
        if isinstance(ctx.val, list):
            return ctx.val[:index] + [item] + ctx.val[index:]
        elif type(ctx.val) is str:
            return ctx.val[:index] + str(item) + ctx.val[index:]
        else:
            return ctx.val
