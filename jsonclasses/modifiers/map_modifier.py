"""module for map modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING, Callable
from .modifier import Modifier
if TYPE_CHECKING:
    from ..types import Types
    from ..ctx import Ctx


class MapModifier(Modifier):
    """Map modifier maps value."""

    def __init__(self, callback: Callable | Types) -> None:
        self.callback = callback

    def transform(self, ctx: Ctx) -> Any:
        from ..types import Types
        if not isinstance(ctx.val, list):
            return ctx.val
        if isinstance(self.callback, Types):
            return [self.callback.modifier.transform(ctx.nval(v)) for v in ctx.val]
        else:
            return [self.callback(v) for v in ctx.val]
