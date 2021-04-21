"""module for validate validator."""
from typing import Callable
from inspect import signature
from ..exceptions import ValidationException
from .validator import Validator
from ..contexts import ValidatingContext


class ValidateValidator(Validator):
    """Validate validator takes a validator."""

    def __init__(self, validate_callable: Callable) -> None:
        if not callable(validate_callable):
            raise ValueError('validator is not callable')
        params_len = len(signature(validate_callable).parameters)
        if params_len > 2 or params_len < 1:
            raise ValueError('not a valid validator')
        self.validate_callable = validate_callable

    def validate(self, context: ValidatingContext) -> None:
        if context.value is None:
            return
        params_len = len(signature(self.validate_callable).parameters)
        if params_len == 1:
            result = self.validate_callable(context.value)
        elif params_len == 2:
            result = self.validate_callable(context.value, context)
        if result is None:
            return
        if result is True:
            return
        if result is False:
            raise ValidationException(
                keypath_messages={context.keypath_root: 'invalid value'},
                root=context.root)
        if isinstance(result, str):
            raise ValidationException(
                keypath_messages={context.keypath_root: result},
                root=context.root)
        raise ValueError('invalid validator')
