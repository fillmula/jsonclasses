"""module for oneoftype validator."""
from __future__ import annotations
from typing import TYPE_CHECKING, Any
from ..excs import ValidationException
from .validator import Validator
from ..rtypes import rtypes
from ..fdef import Fdef, FieldType
if TYPE_CHECKING:
    from ..ctx import Ctx


class OneOfTypeValidator(Validator):
    """One of type validator validates value against a list of available types.
    """

    def __init__(self, type_list: list[Any]) -> None:
        self.type_list = type_list

    def define(self, fdef: Fdef) -> None:
        fdef._field_type = FieldType.UNION
        fdef._raw_union_types = [rtypes(t) for t in self.type_list]

    def validate(self, ctx: Ctx) -> None:
        if ctx.val is None:
            return
        for types in ctx.fdef.raw_union_types:
            try:
                types.validator.validate(ctx)
                return
            except ValidationException:
                continue
        kp = '.'.join([str(k) for k in ctx.keypathr])
        raise ValidationException(
            {'.'.join([str(k) for k in ctx.keypathr]): (f'Value \'{ctx.val}\' at '
                                    f'\'{kp}\' should be '
                                    f'one of type {self.type_list}.')},
            ctx.root)
