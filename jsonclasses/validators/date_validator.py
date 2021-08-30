"""module for date validator."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from datetime import date, datetime
from ..fdef import FieldType
from ..excs import ValidationException
from .type_validator import TypeValidator
if TYPE_CHECKING:
    from ..ctx import Ctx


class DateValidator(TypeValidator):
    """Date validator validate value against date type."""

    def __init__(self):
        super().__init__()
        self.cls = date
        self.field_type = FieldType.DATE

    def transform(self, ctx: Ctx) -> Any:
        if ctx.val is None:
            return None
        elif isinstance(ctx.val, str):
            try:
                return date.fromisoformat(ctx.val[:10])
            except ValueError:
                raise ValidationException({
                    '.'.join([str(k) for k in ctx.keypathr]): 'Date string format error.'
                }, ctx.root)
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
