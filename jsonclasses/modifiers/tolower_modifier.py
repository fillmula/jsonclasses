"""module for tolower modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class ToLowerModifier(Modifier):
    """convert string into lower case"""

    def transform(self, ctx: Ctx) -> Any:
        return ctx.val.lower() if isinstance(ctx.val, str) else ctx.val
