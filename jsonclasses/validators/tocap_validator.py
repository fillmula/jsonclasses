"""module for tocap validator."""
from typing import Any
from .validator import Validator
from ..contexts import TransformingContext


class ToCapValidator(Validator):
    """capitalize string"""

    def transform(self, context: TransformingContext) -> Any:
        if context.value is None:
            return None
        return context.value.capitalize()
