"""module for tonextmonth modifier."""
from __future__ import annotations
from datetime import datetime, date
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx

class ToNextMonModifier(Modifier):
    """Change the month to the next month"""

    def transform(self, ctx: Ctx) -> Any:
        if type(ctx.val) is datetime:
            year, month = divmod(ctx.val.month + 1, 12)
            if month == 0:
                month = 12
                year = year -1
            next_month = datetime(ctx.val.year + year, month, 1)
            return next_month
        if type(ctx.val) is date:
            year, month = divmod(ctx.val.month + 1, 12)
            if month == 0:
                month = 12
                year = year -1
            next_month = date(ctx.val.year + year, month, 1)
            return next_month
        else:
            return ctx.val
