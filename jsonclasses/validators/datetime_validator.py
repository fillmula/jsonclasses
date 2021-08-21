"""module for datetime validator."""
from typing import Any
from datetime import date, datetime
from ..fdef import FieldType
from ..exceptions import ValidationException
from .type_validator import TypeValidator
from ..ctx import Ctx


class DatetimeValidator(TypeValidator):
    """Datetime validator validate value against datetime type."""

    def __init__(self):
        super().__init__()
        self.cls = datetime
        self.field_type = FieldType.DATETIME

    def transform(self, ctx: Ctx) -> Any:
        if ctx.value is None:
            return None
        elif isinstance(ctx.value, str):
            try:
                return datetime.fromisoformat(ctx.value.replace('Z', ''))
            except ValueError:
                raise ValidationException({
                    ctx.keypath_root: 'Datetime string format error.'
                }, ctx.root)
        elif type(ctx.value) is date:
            return datetime(ctx.value.year,
                            ctx.value.month,
                            ctx.value.day, 0, 0, 0)
        else:
            return ctx.value

    def tojson(self, ctx: Ctx) -> Any:
        return None if ctx.value is None else ctx.value.isoformat()[:23] + 'Z'
