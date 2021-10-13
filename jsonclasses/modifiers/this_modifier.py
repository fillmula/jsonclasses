"""module for this modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class ThisModifier(Modifier):
    """Get the owner object of this field.
    """

    def transform(self, ctx: Ctx) -> Any:
        return ctx.owner
