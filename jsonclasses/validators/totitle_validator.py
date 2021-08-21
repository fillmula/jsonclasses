"""module for totitle validator."""
from typing import Any
from .validator import Validator
from ..ctx import Ctx


class ToTitleValidator(Validator):
    """Convert string to title format."""

    def transform(self, ctx: Ctx) -> Any:
        return None if ctx.value is None else ctx.value.title()

