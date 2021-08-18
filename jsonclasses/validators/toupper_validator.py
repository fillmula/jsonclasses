"""module for toupper validator."""
from typing import Any
from .validator import Validator
from ..contexts import TransformingContext


class ToUpperValidator(Validator):
    """convert string into upper case"""

    def transform(self, context: TransformingContext) -> Any:
        if context.value is None:
            return None
        return context.value.upper()
