"""module for operator validator."""
from typing import Callable
from inspect import signature
from ..exceptions import ValidationException
from .validator import Validator
from ..contexts import ValidatingContext


class OpValidator(Validator):
    """Op validator validates with user defined validator."""

    def __init__(self, op_callable: Callable) -> None:
        if not callable(op_callable):
            raise ValueError('op validator is not callable')
        params_len = len(signature(op_callable).parameters)
        if params_len > 4 or params_len < 1:
            raise ValueError('not a valid op validator')
        self.op_callable = op_callable

    def validate(self, context: ValidatingContext) -> None:
        if context.operator is None:
            raise ValidationException(
                {context.keypath_root: 'operator not present'},
                context.root)
        params_len = len(signature(self.op_callable).parameters)
        if params_len == 1:
            result = self.op_callable(context.operator)
        elif params_len == 2:
            result = self.op_callable(context.operator, context.owner)
        elif params_len == 3:
            result = self.op_callable(context.operator, context.owner, context.value)
        elif params_len == 4:
            result = self.op_callable(context.operator, context.owner, context.value, context)
        if result is None:
            return
        if result is True:
            return
        if result is False:
            raise ValidationException(
                keypath_messages={context.keypath_root: 'unauthorized operation'},
                root=context.root)
        if isinstance(result, str):
            raise ValidationException(
                keypath_messages={context.keypath_root: result},
                root=context.root)
        raise ValueError('invalid validator')
