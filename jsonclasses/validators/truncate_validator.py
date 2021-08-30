"""module for truncate validator."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .validator import Validator
if TYPE_CHECKING:
    from ..ctx import Ctx


class TruncateValidator(Validator):
    """Truncate validator truncates value."""

    def __init__(self, maxlen: int) -> None:
        self.maxlen = maxlen

    def transform(self, ctx: Ctx) -> Any:
        return None if ctx.val is None else ctx.val[:self.maxlen]
