"""module for default validator."""
from typing import Any
from .validator import Validator
from ..contexts import TransformingContext


class DefaultValidator(Validator):
    """Default validator assigns value a default value if value is `None`."""

    def __init__(self, default_value: Any) -> None:
        self.default_value = default_value

    def transform(self, context: TransformingContext) -> Any:
        if context.value is not None:
            return context.value
        if callable(self.default_value):
            return self.default_value()
        else:
            return self.default_value
