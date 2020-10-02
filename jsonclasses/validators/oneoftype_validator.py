"""module for oneoftype validator."""
from typing import List, Any
from ..exceptions import ValidationException
from .validator import Validator
from ..contexts import ValidatingContext
from ..types_resolver import resolve_types


class OneOfTypeValidator(Validator):
    """One of type validator validates value against a list of available types.
    """

    def __init__(self, type_list: List[Any]) -> None:
        self.type_list = type_list

    def validate(self, context: ValidatingContext) -> None:
        if context.value is None:
            return
        for raw_type in self.type_list:
            types = resolve_types(raw_type)
            try:
                types.validator.validate(context)
                return
            except ValidationException:
                continue
        raise ValidationException(
            {context.keypath_root: f'Value \'{context.value}\' at \'{context.keypath_root}\' should be one of type {self.type_list}.'},
            context.root
        )
