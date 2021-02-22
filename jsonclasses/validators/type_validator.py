"""module for validator validator."""
from ..exceptions import ValidationException
from ..field_definition import FieldDefinition, FieldType
from ..contexts import ValidatingContext
from .validator import Validator


class TypeValidator(Validator):
    """Abstract validator for checking object's type."""

    def __init__(self) -> None:
        self.cls: type = object
        self.field_type: FieldType = FieldType.ANY
        self.exact_type: bool = False

    def define(self, fdesc: FieldDefinition) -> None:
        fdesc.field_type = self.field_type

    def validate(self, context: ValidatingContext) -> None:
        if context.value is None:
            return
        if self.exact_type:
            if type(context.value) is self.cls:
                return
        else:
            if isinstance(context.value, self.cls):
                return
        raise ValidationException(
            {context.keypath_root: f'Value \'{context.value}\' at \'{context.keypath_root}\' should be {self.cls.__name__}.'},
            context.root
        )
