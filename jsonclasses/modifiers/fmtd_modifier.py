"""module for fmtd modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from datetime import date, datetime
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class FormatDatetimeModifier(Modifier):
    """FormatDatetime modifier format datetime or date"""

    def __init__(self, format: str):
        self.format = format

    def tojson(self, ctx: Ctx) -> Any:
        if isinstance(ctx.val, date) or isinstance(ctx.val, datetime):
            return ctx.val.strftime(self.format)
        elif type(ctx.val) is str:
            dt = datetime.fromisoformat(ctx.val.replace('Z', ''))
            return dt.strftime(self.format)
        else:
            return ctx.val
