"""module for toupper validator."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .validator import Validator
if TYPE_CHECKING:
    from ..ctx import Ctx


class ToUpperValidator(Validator):
    """convert string into upper case"""

    def transform(self, ctx: Ctx) -> Any:
        return None if ctx.val is None else ctx.val.upper()
