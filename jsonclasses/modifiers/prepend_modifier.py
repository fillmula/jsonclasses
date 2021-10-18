"""module for prepend modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class PrependModifier(Modifier):
    """Prepend modifier for adding elements at the beginning of the list."""

    def __init__(self, item: str | int | float | Callable | Types) -> None:
        self.item = item

    def transform(self, ctx: Ctx) -> Any:
        if isinstance(ctx.val, list):
            return [self.resolve_param(self.item, ctx)] + ctx.val
        elif type(ctx.val) is str:
            return self.resolve_param(self.item, ctx) + ctx.val
        else:
            return ctx.val
