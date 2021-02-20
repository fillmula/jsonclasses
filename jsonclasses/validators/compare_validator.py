"""module for compare validator."""
from typing import Callable, cast
from inspect import signature
from ..exceptions import ValidationException
from .validator import Validator
from ..contexts import ValidatingContext


class CompareValidator(Validator):
    """Compare validator validates field value by compare old and new values.
    """

    def __init__(self, compare_callable: Callable) -> None:
        self.compare_callable = compare_callable

    def validate(self, context: ValidatingContext) -> None:
        from ..orm_object import ORMObject
        name = context.keypath_parent
        parent = cast(ORMObject, context.parent)
        if name not in parent.previous_values:
            return
        prev_value = parent.previous_values[name]
        params_len = len(signature(self.compare_callable).parameters)
        if params_len == 2:
            result = self.compare_callable(prev_value, context.value)
        elif params_len == 3:
            result = self.compare_callable(prev_value,
                                           context.value,
                                           context.keypath_parent)
        elif params_len == 4:
            result = self.compare_callable(prev_value,
                                           context.value,
                                           context.keypath_parent,
                                           context.parent)
        elif params_len == 5:
            result = self.compare_callable(prev_value,
                                           context.value,
                                           context.keypath_parent,
                                           context.parent,
                                           context)
        else:
            raise ValueError('wrong number of arguments provided to compare '
                             'validator.')
        if result is not None:
            raise ValidationException(
                keypath_messages={context.keypath_root: result},
                root=context.root)
