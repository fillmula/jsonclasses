"""module for append modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class AppendModifier(Modifier):
    """Insert at modifier for adding an element to the end of list"""

    def __init__(self, item: str | int | float | Callable | Types) -> None:
        self.item = item

    def transform(self, ctx: Ctx) -> Any:
        if isinstance(ctx.val, list):
            return ctx.val + [self.resolve_param(self.item, ctx)]
        elif type(ctx.val) is str:
            return ctx.val + str(self.resolve_param(self.item, ctx))
        else:
            return ctx.val
