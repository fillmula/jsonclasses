"""module for float validator."""
from __future__ import annotations
from typing import TYPE_CHECKING, Any
from .type_validator import TypeValidator
from ..fdef import FieldType
if TYPE_CHECKING:
    from ..ctx import Ctx


class FloatValidator(TypeValidator):
    """Date validator validate value against float type."""

    def __init__(self):
        super().__init__()
        self.cls = float
        self.field_type = FieldType.FLOAT

    def transform(self, ctx: Ctx) -> Any:
        if ctx.value is None:
            return None
        if type(ctx.value) is int:
            return float(ctx.value)
        return ctx.value
