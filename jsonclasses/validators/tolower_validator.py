"""module for tolower validator."""
from typing import Any
from .validator import Validator
from ..ctx import Ctx


class ToLowerValidator(Validator):
    """convert string into lower case"""

    def transform(self, ctx: Ctx) -> Any:
        if context.value is None:
            return None
        return context.value.lower()
