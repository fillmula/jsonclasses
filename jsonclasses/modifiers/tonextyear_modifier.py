"""module for tonextyear modifier."""
from __future__ import annotations
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx

class ToNextYearModifier(Modifier):
    """Change the year to the next year"""

    def transform(self, ctx: Ctx) -> Any:
        if type(ctx.val) is datetime:
            return (ctx.val+relativedelta(years=1)).replace(microsecond=0, second=0, minute=0, hour=0, day=1, month=1)
        if type(ctx.val) is date:
            return (ctx.val+relativedelta(years=1)).replace(day=1, month=1)
        else:
            return ctx.val
