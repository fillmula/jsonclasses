"""module for validator validator."""
from ..exceptions import ValidationException
from .validator import Validator
from ..contexts import ValidatingContext


class InvalidValidator(Validator):
    """A validator that turns value into invalid."""

    def validate(self, context: ValidatingContext) -> None:
        """Raises invalid exception."""
        raise ValidationException(
            {context.keypath_root: f'Value \'{context.value}\' at \'{context.keypath_root}\' is invalid.'},
            context.root
        )
