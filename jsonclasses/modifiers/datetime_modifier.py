"""module for datetime modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from datetime import date, datetime
from ..fdef import FType
from .type_modifier import TypeModifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class DatetimeModifier(TypeModifier):
    """Datetime modifier validate value against datetime type."""

    def __init__(self):
        super().__init__()
        self.cls = datetime
        self.ftype = FType.DATETIME

    def transform(self, ctx: Ctx) -> Any:
        if ctx.val is None:
            return None
        elif isinstance(ctx.val, str):
            try:
                return datetime.fromisoformat(ctx.val.replace('Z', ''))
            except ValueError:
                ctx.raise_vexc('wrong datetime format')
        elif type(ctx.val) is date:
            return datetime(ctx.val.year,
                            ctx.val.month,
                            ctx.val.day, 0, 0, 0)
        else:
            return ctx.val

    def tojson(self, ctx: Ctx) -> Any:
        return None if ctx.val is None else ctx.val.isoformat()[:23] + 'Z'
