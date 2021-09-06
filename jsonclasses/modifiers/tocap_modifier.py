"""module for tocap modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class ToCapModifier(Modifier):
    """capitalize string"""

    def transform(self, ctx: Ctx) -> Any:
        return ctx.val.capitalize() if isinstance(ctx.val, str) else ctx.val
