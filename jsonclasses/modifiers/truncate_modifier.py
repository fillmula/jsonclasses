"""module for truncate modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class TruncateModifier(Modifier):
    """Truncate modifier truncates value."""

    def __init__(self, maxlen: int) -> None:
        self.maxlen = maxlen

    def transform(self, ctx: Ctx) -> Any:
        return None if ctx.val is None else ctx.val[:self.maxlen]
