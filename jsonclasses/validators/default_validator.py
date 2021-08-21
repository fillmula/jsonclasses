"""module for default validator."""
from typing import Any
from .validator import Validator
from ..ctx import Ctx


class DefaultValidator(Validator):
    """Default validator assigns value a default value if value is `None`."""

    def __init__(self, default: Any) -> None:
        self.default = default

    def transform(self, ctx: Ctx) -> Any:
        if ctx.value is not None:
            return ctx.value
        if callable(self.default):
            return self.default()
        else:
            return self.default
