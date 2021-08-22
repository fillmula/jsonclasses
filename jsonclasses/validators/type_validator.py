"""module for validator validator."""
from __future__ import annotations
from typing import TYPE_CHECKING
from ..exceptions import ValidationException
from ..fdef import Fdef, FieldType
from .validator import Validator
if TYPE_CHECKING:
    from ..ctx import Ctx


class TypeValidator(Validator):
    """Abstract validator for checking object's type."""

    def __init__(self) -> None:
        self.cls: type = object
        self.field_type: FieldType = FieldType.ANY
        self.exact_type: bool = False

    def define(self, fdef: Fdef) -> None:
        fdef._field_type = self.field_type

    def validate(self, ctx: Ctx) -> None:
        if ctx.value is None:
            return
        if self.exact_type:
            if type(ctx.value) is self.cls:
                return
        else:
            if isinstance(ctx.value, self.cls):
                return
        raise ValidationException(
            {'.'.join([str(k) for k in ctx.keypathr]): f'Value \'{ctx.value}\' at \'{kp}\' should be {self.cls.__name__}.'},
            ctx.root
        )
