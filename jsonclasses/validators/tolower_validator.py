"""module for tolower validator."""
from typing import Any
from .validator import Validator
from ..contexts import TransformingContext


class ToLowerValidator(Validator):
    """convert string into lower case"""

    def transform(self, context: TransformingContext) -> Any:
        if context.value is None:
            return None
        return context.value.lower()
