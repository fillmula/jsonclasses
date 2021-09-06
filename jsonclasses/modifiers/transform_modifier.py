"""module for transform modifier."""
from __future__ import annotations
from typing import Callable, Any, TYPE_CHECKING
from inspect import signature
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class TransformModifier(Modifier):
    """Transform modifier transforms value."""

    def __init__(self, transformer: Callable) -> None:
        if not callable(transformer):
            raise ValueError('transformer is not callable')
        params_len = len(signature(transformer).parameters)
        if params_len > 2 or params_len < 1:
            raise ValueError('not a valid transformer')
        self.transformer = transformer

    def transform(self, ctx: Ctx) -> Any:
        if ctx.val is None:
            return None
        params_len = len(signature(self.transformer).parameters)
        if params_len == 1:
            return self.transformer(ctx.val)
        elif params_len == 2:
            return self.transformer(ctx.val, ctx)
