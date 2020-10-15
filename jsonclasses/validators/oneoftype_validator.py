"""module for oneoftype validator."""
from typing import Any
from ..exceptions import ValidationException
from .validator import Validator
from ..contexts import ValidatingContext
from ..types_resolver import resolve_types
from ..fields import FieldDescription, FieldType


class OneOfTypeValidator(Validator):
    """One of type validator validates value against a list of available types.
    """

    def __init__(self, type_list: list[Any]) -> None:
        self.type_list = type_list

    def define(self, fdesc: FieldDescription) -> None:
        fdesc.field_type = FieldType.UNION
        fdesc.union_types = [resolve_types(t) for t in self.type_list]

    def validate(self, context: ValidatingContext) -> None:
        if context.value is None:
            return
        for types in context.fdesc.union_types:
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
