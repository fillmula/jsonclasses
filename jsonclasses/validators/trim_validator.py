"""module for trim validator."""
from typing import Any
from .validator import Validator
from ..contexts import TransformingContext


class TrimValidator(Validator):
    """Trim validator trims string values."""

    def transform(self, context: TransformingContext) -> Any:
        if context.value is None:
            return None
        return context.value.strip()
