"""module for onsave modifier."""
from __future__ import annotations
from typing import Callable, Any, cast, TYPE_CHECKING
from inspect import signature
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class OnWriteModifier(Modifier):
    """On write modifier is called when field has a new value and saving is
    triggered.
    """

    def __init__(self, callback: Callable) -> None:
        if not callable(callback):
            raise ValueError('onwrite callback is not callable')
        params_len = len(signature(callback).parameters)
        if params_len > 2:
            raise ValueError('not a valid onwrite callback')
        self.callback = callback

    def serialize(self, ctx: Ctx) -> Any:
        from ..jobject import JObject
        name = ctx.keypathp[-1]
        parent = cast(JObject, ctx.parent)
        if not parent.is_new and name not in parent.modified_fields:
            return ctx.val
        params_len = len(signature(self.callback).parameters)
        if params_len == 0:
            self.callback()
        elif params_len == 1:
            self.callback(ctx.val)
        elif params_len == 2:
            self.callback(ctx.val, ctx)
        return ctx.val
