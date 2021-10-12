"""module for tonextsec modifier."""
from __future__ import annotations
from datetime import datetime, timedelta
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx

class ToNextSecModifier(Modifier):
    """Change the second to the next second"""

    def transform(self, ctx: Ctx) -> Any:
        return (ctx.val+timedelta(seconds=1)).replace(microsecond=0) if type(ctx.val) is datetime else ctx.val
