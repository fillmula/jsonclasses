"""module for onupdate validator."""
from __future__ import annotations
from typing import Callable, Any, cast, TYPE_CHECKING
from inspect import signature
from .validator import Validator
if TYPE_CHECKING:
    from ..ctx import Ctx


class OnUpdateValidator(Validator):
    """On update validator is called when value is modified and saving is
    triggered.
    """

    def __init__(self, callback: Callable) -> None:
        if not callable(callback):
            raise ValueError('onupdate argument is not callable')
        params_len = len(signature(callback).parameters)
        if params_len > 3:
            raise ValueError('not a valid onupdate callable')
        self.callback = callback

    def serialize(self, ctx: Ctx) -> Any:
        from ..jobject import JObject
        name = ctx.keypathp[-1]
        parent = cast(JObject, ctx.parent)
        if name not in parent.previous_values:
            return ctx.val
        prev_value = parent.previous_values[name]
        params_len = len(signature(self.callback).parameters)
        if params_len == 0:
            self.callback()
        elif params_len == 1:
            self.callback(ctx.val)
        elif params_len == 2:
            self.callback(prev_value, ctx.val)
        elif params_len == 3:
            self.callback(prev_value,
                          ctx.val,
                          ctx)
        return ctx.val
