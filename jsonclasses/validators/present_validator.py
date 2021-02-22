"""module for required validator."""
from ..field_definition import FieldDefinition
from ..exceptions import ValidationException
from .validator import Validator
from ..contexts import ValidatingContext


class PresentValidator(Validator):
    """Present validator marks a field as present. When validating, if no value
    is present in this field, validation will fail. This is useful for foreign
    key fields to do required validation.
    """

    def define(self, fdesc: FieldDefinition) -> None:
        fdesc.required = True

    def validate(self, context: ValidatingContext) -> None:
        if context.value is None:
            raise ValidationException(
                {context.keypath_root: (f'Value at \'{context.keypath_root}\''
                                        ' should be present.')},
                context.root)
