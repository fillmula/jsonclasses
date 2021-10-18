"""module for replacer modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING, Callable
from re import sub
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types

class ReplacerModifier(Modifier):
    """Sub modifier substitudes value against a regular expression."""

    def __init__(self, reg: str | Callable | Types, rep: str | Callable | Types) -> None:
        self.reg = reg
        self.rep = rep

    def transform(self, ctx: Ctx) -> Any:
        reg = self.resolve_param(self.reg, ctx)
        rep = self.resolve_param(self.rep, ctx)
        return sub(reg, rep, ctx.val) if type(ctx.val) is str else ctx.val
