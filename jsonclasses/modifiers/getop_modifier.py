"""module for getop modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class GetOpModifier(Modifier):
    """Get the operator object this action.
    """

    def transform(self, ctx: Ctx) -> Any:
        return ctx.operator
