"""module for month modifier."""
from __future__ import annotations
from datetime import date, datetime
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx

class ToBoMonModifier(Modifier):
    """
    ToBoMonth Modifier transforms date or datetime into the beginning of the
    month
    """

    def transform(self, ctx: Ctx) -> Any:
        if type(ctx.val) is datetime:
            return ctx.val.replace(microsecond=0, second=0, minute=0, hour=0, day=1)
        if type(ctx.val) is date:
            return ctx.val.replace(day=1)
        else:
            return ctx.val
