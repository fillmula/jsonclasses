"""module for filter modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING, Callable
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class FilterModifier(Modifier):
    """Filter modifier filters value."""

    def __init__(self, callback: Callable | Types) -> None:
        self.callback = callback

    def transform(self, ctx: Ctx) -> Any:
        from ..types import Types
        if not isinstance(ctx.val, list):
            return ctx.val
        if isinstance(self.callback, Types):
            result = []
            for v in ctx.val:
                tsfmd = self.callback.modifier.transform(ctx.nval(v))
                try:
                    self.callback.modifier.validate(ctx.nval(tsfmd))
                    result.append(v)
                except:
                    continue
            return result
        else:
            result = []
            for v in ctx.val:
                callbackv = self.callback(v)
                if callbackv is None or callbackv is True:
                    result.append(v)
            return result
