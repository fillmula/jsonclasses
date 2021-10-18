"""module for default modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING, Callable
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class DefaultModifier(Modifier):
    """Default modifier assigns field a default value if value is `None`."""

    def __init__(self, default: Any | Callable | Types) -> None:
        self.default = default

    def transform(self, ctx: Ctx) -> Any:
        if ctx.val is not None:
            return ctx.val
        if callable(self.default):
            return self.default()
        else:
            return self.resolve_param(self.default, ctx)
