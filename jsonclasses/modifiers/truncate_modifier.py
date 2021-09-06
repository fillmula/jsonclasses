"""module for truncate modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class TruncateModifier(Modifier):
    """Truncate modifier truncates value."""

    def __init__(self, mlen: int) -> None:
        self.mlen = mlen

    def transform(self, ctx: Ctx) -> Any:
        return ctx.val[:self.mlen] if hasattr(ctx.val, '__len__') else ctx.val
