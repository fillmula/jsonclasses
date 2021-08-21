"""module for oneoftype validator."""
from typing import Any
from ..exceptions import ValidationException
from .validator import Validator
from ..ctx import Ctx
from ..rtypes import rtypes
from ..fdef import Fdef, FieldType


class OneOfTypeValidator(Validator):
    """One of type validator validates value against a list of available types.
    """

    def __init__(self, type_list: list[Any]) -> None:
        self.type_list = type_list

    def define(self, fdef: Fdef) -> None:
        fdef._field_type = FieldType.UNION
        fdef._raw_union_types = [rtypes(t) for t in self.type_list]

    def validate(self, ctx: Ctx) -> None:
        if ctx.value is None:
            return
        for types in ctx.fdef.raw_union_types:
            try:
                types.validator.validate(ctx)
                return
            except ValidationException:
                continue
        raise ValidationException(
            {ctx.keypath_root: (f'Value \'{ctx.value}\' at '
                                    f'\'{ctx.keypath_root}\' should be '
                                    f'one of type {self.type_list}.')},
            ctx.root)
