"""module for tocap validator."""
from typing import Any, cast
from .validator import Validator
from ..ctx import Ctx


class ToCapValidator(Validator):
    """capitalize string"""

    def transform(self, ctx: Ctx) -> Any:
        return None if ctx.value is None else ctx.value.capitalize()
