"""module for date validator."""
from typing import Any
from datetime import date, datetime
from ..fdef import FieldType
from ..exceptions import ValidationException
from .type_validator import TypeValidator
from ..ctx import Ctx


class DateValidator(TypeValidator):
    """Date validator validate value against date type."""

    def __init__(self):
        super().__init__()
        self.cls = date
        self.field_type = FieldType.DATE

    def transform(self, ctx: Ctx) -> Any:
        if ctx.value is None:
            return None
        elif isinstance(ctx.value, str):
            try:
                return date.fromisoformat(ctx.value[:10])
            except ValueError:
                raise ValidationException({
                    ctx.keypath_root: 'Date string format error.'
                }, ctx.root)
        elif type(ctx.value) == datetime:
            return date(ctx.value.year,
                        ctx.value.month,
                        ctx.value.day)
        else:
            return ctx.value

    def tojson(self, ctx: Ctx) -> Any:
        return None if ctx.value is None else self._jsondate(ctx.value)

    def _jsondate(self, d: date) -> str:
        return d.isoformat() + 'T00:00:00.000Z'
