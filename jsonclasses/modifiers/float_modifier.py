"""module for float modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING, Any
from .type_modifier import TypeModifier
from ..fdef import FType
if TYPE_CHECKING:
    from ..ctx import Ctx


class FloatModifier(TypeModifier):
    """Date modifier validate value against float type."""

    def __init__(self):
        super().__init__()
        self.cls = float
        self.ftype = FType.FLOAT

    def transform(self, ctx: Ctx) -> Any:
        if ctx.val is None:
            return None
        if type(ctx.val) is int:
            return float(ctx.val)
        return ctx.val
