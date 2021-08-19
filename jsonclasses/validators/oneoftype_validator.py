"""module for oneoftype validator."""
from typing import Any
from ..exceptions import ValidationException
from .validator import Validator
from ..ctxs import VCtx
from ..rtypes import rtypes
from ..fdef import Fdef, FieldType


class OneOfTypeValidator(Validator):
    """One of type validator validates value against a list of available types.
    """

    def __init__(self, type_list: list[Any]) -> None:
        self.type_list = type_list

    def define(self, fdef: Fdef) -> None:
        fdef._field_type = FieldType.UNION
        fdef._union_types = [rtypes(t) for t in self.type_list]

    def validate(self, context: VCtx) -> None:
        if context.value is None:
            return
        for types in context.fdef.raw_union_types:
            try:
                types.validator.validate(context)
                return
            except ValidationException:
                continue
        raise ValidationException(
            {context.keypath_root: (f'Value \'{context.value}\' at '
                                    f'\'{context.keypath_root}\' should be '
                                    f'one of type {self.type_list}.')},
            context.root)
