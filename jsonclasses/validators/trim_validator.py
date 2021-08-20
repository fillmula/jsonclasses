"""module for trim validator."""
from typing import Any
from .validator import Validator
from ..ctx import TCtx


class TrimValidator(Validator):
    """Trim validator trims string values."""

    def transform(self, context: TCtx) -> Any:
        if context.value is None:
            return None
        if not isinstance(context.value, str):
            return context.value
        return context.value.strip()
