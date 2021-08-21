"""module for toupper validator."""
from typing import Any
from .validator import Validator
from ..ctx import Ctx


class ToUpperValidator(Validator):
    """convert string into upper case"""

    def transform(self, ctx: Ctx) -> Any:
        return None if ctx.value is None else ctx.value.upper()
