"""module for validator validator."""
from ..exceptions import ValidationException
from ..fdef import Fdef, FieldType
from ..ctx import Ctx
from .validator import Validator


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
            {ctx.keypath_root: f'Value \'{ctx.value}\' at \'{ctx.keypath_root}\' should be {self.cls.__name__}.'},
            ctx.root
        )
