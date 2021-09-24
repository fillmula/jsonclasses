"""module for date modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from datetime import date, datetime
from ..fdef import FType
from .type_modifier import TypeModifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class DateModifier(TypeModifier):
    """Date modifier validate value against date type."""

    def __init__(self):
        super().__init__()
        self.cls = date
        self.ftype = FType.DATE

    def transform(self, ctx: Ctx) -> Any:
        if ctx.val is None:
            return None
        elif isinstance(ctx.val, str):
            try:
                return date.fromisoformat(ctx.val[:10])
            except ValueError:
                ctx.raise_vexc('wrong date format')
        elif type(ctx.val) == datetime:
            return date(ctx.val.year,
                        ctx.val.month,
                        ctx.val.day)
        else:
            return ctx.val

    def tojson(self, ctx: Ctx) -> Any:
        return None if ctx.val is None else self._jsondate(ctx.val)

    def _jsondate(self, d: date) -> str:
        return d.isoformat() + 'T00:00:00.000Z'
