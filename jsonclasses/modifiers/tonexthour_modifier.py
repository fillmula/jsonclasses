"""module for tonexthour modifier."""
from __future__ import annotations
from datetime import datetime, timedelta
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx

class ToNextHourModifier(Modifier):
    """Change the hour to the next hour"""

    def transform(self, ctx: Ctx) -> Any:
        return (ctx.val+timedelta(hours=1)).replace(microsecond=0, second=0, minute=0) if type(ctx.val) is datetime else ctx.val
