"""module for month modifier."""
from __future__ import annotations
from datetime import date, datetime
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx

class MonthModifier(Modifier):
    """"""

    def transform(self, ctx: Ctx) -> Any:
        is_date = type(ctx.val) is datetime or type(ctx.val) is date
        return ctx.val.replace(microsecond=0, second=0, minute=0) if is_date  else ctx.val
