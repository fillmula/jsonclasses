"""module for fmtd modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING, Callable
from datetime import date, datetime
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class FormatDatetimeModifier(Modifier):
    """FormatDatetime modifier format datetime or date"""

    def __init__(self, format: str | Callable | Types):
        self.format = format

    def tojson(self, ctx: Ctx) -> Any:
        if isinstance(ctx.val, date) or isinstance(ctx.val, datetime):
            return ctx.val.strftime(self.resolve_param(self.format, ctx))
        elif type(ctx.val) is str:
            dt = datetime.fromisoformat(ctx.val.replace('Z', ''))
            return dt.strftime(self.resolve_param(self.format, ctx))
        else:
            return ctx.val
