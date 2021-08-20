"""module for trim validator."""
from typing import Any
from .validator import Validator
from ..ctx import Ctx


class TrimValidator(Validator):
    """Trim validator trims string values."""

    def transform(self, ctx: Ctx) -> Any:
        if context.value is None:
            return None
        if not isinstance(context.value, str):
            return context.value
        return context.value.strip()
