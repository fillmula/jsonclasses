"""module for inverse modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING, Callable
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types

class InverseModifier(Modifier):
    """Inverse modifier changes the value to false if value is true, vice versa."""

    def transform(self, ctx: Ctx) -> Any:
        return not ctx.val if type(ctx.val) is bool else ctx.val
