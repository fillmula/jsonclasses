"""module for tobohour modifier."""
from __future__ import annotations
from datetime import datetime
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx

class ToBoHourModifier(Modifier):
    """
    ToBoHour Modifier transforms datetime into the beginning of the hour
    """

    def transform(self, ctx: Ctx) -> Any:
        return ctx.val.replace(microsecond=0, second=0, minute=0) if type(ctx.val) is datetime else ctx.val
