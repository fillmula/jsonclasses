"""module for tocap validator."""
from typing import Any
from .validator import Validator
from ..ctx import Ctx


class ToCapValidator(Validator):
    """capitalize string"""

    def transform(self, ctx: Ctx) -> Any:
        if context.value is None:
            return None
        return context.value.capitalize()
