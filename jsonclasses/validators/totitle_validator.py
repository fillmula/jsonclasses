"""module for totitle validator."""
from typing import Any
from .validator import Validator
from ..contexts import TransformingContext


class ToTitleValidator(Validator):
    """Convert string to title format."""

    def transform(self, context: TransformingContext) -> Any:
        if context.value is None:
            return None
        return context.value.title()
