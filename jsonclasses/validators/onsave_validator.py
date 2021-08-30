"""module for onsave validator."""
from __future__ import annotations
from typing import Callable, Any, TYPE_CHECKING
from inspect import signature
from .validator import Validator
if TYPE_CHECKING:
    from ..ctx import Ctx


class OnSaveValidator(Validator):
    """On save validator is called when saving is triggered."""

    def __init__(self, callback: Callable) -> None:
        if not callable(callback):
            raise ValueError('onsave argument is not callable')
        params_len = len(signature(callback).parameters)
        if params_len > 1:
            raise ValueError('not a valid onsave callable')
        self.callback = callback

    def serialize(self, ctx: Ctx) -> Any:
        params_len = len(signature(self.callback).parameters)
        if params_len == 0:
            self.callback()
        elif params_len == 1:
            self.callback(ctx.val)
        return ctx.val
