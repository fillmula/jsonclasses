"""module for truncate validator."""
from typing import Any
from .validator import Validator
from ..ctxs import TCtx


class TruncateValidator(Validator):
    """Truncate validator truncates value."""

    def __init__(self, max_length: int) -> None:
        self.max_length = max_length

    def transform(self, context: TCtx) -> Any:
        if context.value is None:
            return None
        if context.value.__len__() > self.max_length:
            return context.value[:self.max_length]
        return context.value
