"""module for replace modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from re import sub
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx

class SubModifier(Modifier):
    """Sub modifier substitudes value against a regular expression."""

    def __init__(self, reg: str, rep: str) -> None:
        self.reg = reg
        self.rep = rep

    def transform(self, ctx: Ctx) -> Any:
        return sub(self.reg, self.rep, ctx.val) if type(ctx.val) is str else ctx.val
