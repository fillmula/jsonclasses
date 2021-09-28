"""module for join modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx

class JoinModifier(Modifier):
    """Join modifier Joins a list of string values into a string."""

    def __init__(self, sep: str) -> None:
        self.sep = sep

    def transform(self, ctx: Ctx) -> Any:
        return self.sep.join(ctx.val) if isinstance(ctx.val, list) else ctx.val
