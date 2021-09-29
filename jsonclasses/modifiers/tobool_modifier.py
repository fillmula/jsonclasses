"""module for tobool modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class ToBoolModifier(Modifier):
    """ToBool Modifier transforms value into a bool"""

    def transform(self, ctx: Ctx) -> Any:
        return bool(ctx.val)
