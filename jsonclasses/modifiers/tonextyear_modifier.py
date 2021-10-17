"""module for tonextyear modifier."""
from __future__ import annotations
from datetime import datetime, date
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx

class ToNextYearModifier(Modifier):
    """The next first day of year after this date or datetime."""

    def transform(self, ctx: Ctx) -> Any:
        if type(ctx.val) is datetime:
            return datetime(ctx.val.year + 1, 1, 1, 0, 0, 0, 0)
        if type(ctx.val) is date:
            return date(ctx.val.year + 1, 1, 1)
        else:
            return ctx.val
