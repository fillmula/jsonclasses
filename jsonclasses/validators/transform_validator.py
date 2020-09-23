"""module for transform validator."""
from typing import Callable, Any
from .validator import Validator
from ..contexts import TransformingContext


class TransformValidator(Validator):
    """Transform validator transforms value."""

    def __init__(self, transformer: Callable) -> None:
        self.transformer = transformer

    def transform(self, context: TransformingContext) -> Any:
        if context.value is None:
            return None
        return self.transformer(context.value)
