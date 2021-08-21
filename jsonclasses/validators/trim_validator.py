"""module for trim validator."""
from typing import Any
from .validator import Validator
from ..ctx import Ctx


class TrimValidator(Validator):
    """Trim validator trims string values."""

    def transform(self, ctx: Ctx) -> Any:
        return None if ctx.value is None else ctx.value.strip()

