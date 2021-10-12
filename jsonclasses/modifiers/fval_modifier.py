"""module for fval modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class FValModifier(Modifier):
    """Get value at field from a JSONClass object.
    """

    def __init__(self, field_name: str) -> None:
        self.field_name = field_name

    def transform(self, ctx: Ctx) -> Any:
        if ctx.val is None:
            return None
        return getattr(ctx.val, self.field_name)
