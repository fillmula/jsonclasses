"""module for trim validator."""
from typing import Any
from .validator import Validator
from ..contexts import ValidatingContext, TransformingContext


class TrimValidator(Validator):
    """Trim validator trims string values."""

    def validate(self, context: ValidatingContext) -> None:
        pass

    def transform(self, context: TransformingContext) -> Any:
        if context.value is None:
            return None
        return context.value.strip()
