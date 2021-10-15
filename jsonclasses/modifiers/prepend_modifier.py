"""module for prepend modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING, Any
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class PrependModifier(Modifier):
    """Prepend modifier for adding elements at the beginning of the list."""

    def __init__(self, item: str | int | float) -> None:
        self.item = item

    def transform(self, ctx: Ctx) -> Any:
        if isinstance(ctx.val, list):
            return [self.item] + ctx.val
        elif type(ctx.val) is str:
            return self.item + ctx.val
        else:
            return ctx.val
