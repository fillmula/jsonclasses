"""module for default validator."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .validator import Validator
if TYPE_CHECKING:
    from ..ctx import Ctx


class DefaultValidator(Validator):
    """Default validator assigns field a default value if value is `None`."""

    def __init__(self, default: Any) -> None:
        self.default = default

    def transform(self, ctx: Ctx) -> Any:
        if ctx.val is not None:
            return ctx.val
        if callable(self.default):
            return self.default()
        else:
            return self.default
