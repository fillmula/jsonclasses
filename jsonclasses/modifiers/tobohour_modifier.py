"""module for tobohour modifier."""
from __future__ import annotations
from datetime import datetime
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx

class ToBoHourModifier(Modifier):
    """Remove the microsecond, second and minute infromation from datetime and
    save the date, hour, etc."""

    def transform(self, ctx: Ctx) -> Any:
        return ctx.val.replace(microsecond=0, second=0, minute=0) if type(ctx.val) is datetime else ctx.val
