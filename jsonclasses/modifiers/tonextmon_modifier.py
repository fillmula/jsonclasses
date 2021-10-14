"""module for tonextmonth modifier."""
from __future__ import annotations
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx

class ToNextMonModifier(Modifier):
    """Change the month to the next month"""

    def transform(self, ctx: Ctx) -> Any:
        if type(ctx.val) is datetime:
            return (ctx.val+relativedelta(months=1)).replace(microsecond=0, second=0, minute=0, hour=0, day=1)
        if type(ctx.val) is date:
            return (ctx.val+relativedelta(months=1)).replace(day=1)
        else:
            return ctx.val
