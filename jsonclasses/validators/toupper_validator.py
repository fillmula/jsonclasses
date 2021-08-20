"""module for toupper validator."""
from typing import Any
from .validator import Validator
from ..ctx import TCtx


class ToUpperValidator(Validator):
    """convert string into upper case"""

    def transform(self, context: TCtx) -> Any:
        if context.value is None:
            return None
        return context.value.upper()
