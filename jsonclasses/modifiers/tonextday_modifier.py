"""module for tonextday modifier."""
from __future__ import annotations
from datetime import datetime, date, timedelta
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx

class ToNextDayModifier(Modifier):
    """Change the day to the next day"""

    def transform(self, ctx: Ctx) -> Any:
        if type(ctx.val) is datetime:
            return (ctx.val+timedelta(days=1)).replace(microsecond=0, second=0, minute=0, hour=0)
        if type(ctx.val) is date:
            return ctx.val+timedelta(days=1)
        else:
            return ctx.val
