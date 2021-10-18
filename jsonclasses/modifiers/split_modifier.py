"""module for split modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING, Callable
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class SplitModifier(Modifier):
    """Split modifier split value."""

    def __init__(self, sep: str | Callable | Types) -> None:
        self.sep = sep

    def transform(self, ctx: Ctx) -> Any:
        return ctx.val.split(self.resolve_param(self.sep, ctx)) if type(ctx.val) is str else ctx.val
