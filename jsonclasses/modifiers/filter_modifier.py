"""module for filter modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING, Callable, Container
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx

class FilterModifier(Modifier):
    """Filter modifier filters number value."""

    def __init__(self, callback: Callable) -> None:
        if not callable(callback):
            raise ValueError('filter callback is not callable')
        self.callback = callback


    def transform(self, ctx: Ctx) -> Any:
        if isinstance(ctx.val, list):
            return list(filter(self.callback , ctx.val))
        else:
            return ctx.val
