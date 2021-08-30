"""module for tolower validator."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .validator import Validator
if TYPE_CHECKING:
    from ..ctx import Ctx


class ToLowerValidator(Validator):
    """convert string into lower case"""

    def transform(self, ctx: Ctx) -> Any:
        return None if ctx.val is None else ctx.val.lower()
