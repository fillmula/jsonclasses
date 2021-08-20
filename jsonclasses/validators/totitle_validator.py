"""module for totitle validator."""
from typing import Any
from .validator import Validator
from ..ctx import TCtx


class ToTitleValidator(Validator):
    """Convert string to title format."""

    def transform(self, context: TCtx) -> Any:
        if context.value is None:
            return None
        return context.value.title()
