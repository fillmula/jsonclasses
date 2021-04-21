"""module for transform validator."""
from typing import Callable, Any
from inspect import signature
from .validator import Validator
from ..contexts import TransformingContext


class TransformValidator(Validator):
    """Transform validator transforms value."""

    def __init__(self, transformer: Callable) -> None:
        if not callable(transformer):
            raise ValueError('transformer is not callable')
        params_len = len(signature(transformer).parameters)
        if params_len > 2 or params_len < 1:
            raise ValueError('not a valid transformer')
        self.transformer = transformer

    def transform(self, context: TransformingContext) -> Any:
        if context.value is None:
            return None
        params_len = len(signature(self.transformer).parameters)
        if params_len == 1:
            return self.transformer(context.value)
        elif params_len == 2:
            return self.transformer(context.value, context)
