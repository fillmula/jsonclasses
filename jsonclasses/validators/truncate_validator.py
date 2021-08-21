"""module for truncate validator."""
from typing import Any
from .validator import Validator
from ..ctx import Ctx


class TruncateValidator(Validator):
    """Truncate validator truncates value."""

    def __init__(self, maxlen: int) -> None:
        self.maxlen = maxlen

    def transform(self, ctx: Ctx) -> Any:
        return None if ctx.value is None else ctx.value[:self.maxlen]
