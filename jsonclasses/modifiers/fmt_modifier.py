"""module for fmt modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING, Callable
from inspect import signature
from .modifier import Modifier
if TYPE_CHECKING:
    from ..types import Types
    from ..ctx import Ctx


class FmtModifier(Modifier):
    """Fmt modifier formats value when presented."""

    def __init__(self, formatter: Callable | Types) -> None:
        super().__init__()
        if callable(formatter):
            params_len = len(signature(formatter).parameters)
            if params_len > 2 or params_len < 1:
                raise ValueError('not a valid formatter callable')
        self.formatter = formatter

    def tojson(self, ctx: Ctx) -> Any:
        from ..types import Types
        if isinstance(self.formatter, Types):
            return self.formatter.modifier.transform(ctx)
        if ctx.val is None:
            return None
        params_len = len(signature(self.formatter).parameters)
        if params_len == 1:
            return self.formatter(ctx.val)
        elif params_len == 2:
            return self.formatter(ctx.val, ctx)
