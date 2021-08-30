"""module for validator validator."""
from __future__ import annotations
from typing import TYPE_CHECKING
from ..excs import ValidationException
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
        if ctx.val is None:
            return
        if self.exact_type:
            if type(ctx.val) is self.cls:
                return
        else:
            if isinstance(ctx.val, self.cls):
                return
        kp = '.'.join([str(k) for k in ctx.keypathr])
        raise ValidationException(
            {kp: f'Value \'{ctx.val}\' at \'{kp}\' should be {self.cls.__name__}.'},
            ctx.root
        )
