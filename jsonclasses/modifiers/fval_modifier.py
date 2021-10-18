"""module for fval modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING, Callable
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class FValModifier(Modifier):
    """Get value at field from a JSONClass object.
    """

    def __init__(self, field_name: str | Callable | Types) -> None:
        self.field_name = field_name

    def transform(self, ctx: Ctx) -> Any:
        if ctx.val is None:
            return None
        return getattr(ctx.val, self.resolve_param(self.field_name, ctx))
