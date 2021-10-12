"""module for day modifier."""
from __future__ import annotations
from datetime import date, datetime
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx

class ToBoDayModifier(Modifier):
    """
    ToBoDay Modifier transforms date or datetime into the beginning of the
    day
    """

    def transform(self, ctx: Ctx) -> Any:
        if type(ctx.val) is datetime:
            return ctx.val.replace(microsecond=0, second=0, minute=0, hour=0)
        if type(ctx.val) is date:
            return ctx.val
        else:
            return ctx.val
