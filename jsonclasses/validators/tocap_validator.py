"""module for tocap validator."""
from typing import Any
from .validator import Validator
from ..ctxs import TCtx


class ToCapValidator(Validator):
    """capitalize string"""

    def transform(self, context: TCtx) -> Any:
        if context.value is None:
            return None
        return context.value.capitalize()
