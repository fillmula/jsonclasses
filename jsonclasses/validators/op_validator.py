"""module for operator validator."""
from __future__ import annotations
from typing import Callable, TYPE_CHECKING
from inspect import signature
from ..exceptions import ValidationException
from .validator import Validator
if TYPE_CHECKING:
    from ..ctx import Ctx


class OpValidator(Validator):
    """Op validator validates with user defined validator."""

    def __init__(self, op_callable: Callable) -> None:
        if not callable(op_callable):
            raise ValueError('op validator is not callable')
        params_len = len(signature(op_callable).parameters)
        if params_len > 4 or params_len < 1:
            raise ValueError('not a valid op validator')
        self.op_callable = op_callable

    def validate(self, ctx: Ctx) -> None:
        if ctx.operator is None:
            raise ValidationException(
                {ctx.keypath_root: 'operator not present'},
                ctx.root)
        params_len = len(signature(self.op_callable).parameters)
        if params_len == 1:
            result = self.op_callable(ctx.operator)
        elif params_len == 2:
            result = self.op_callable(ctx.operator, ctx.owner)
        elif params_len == 3:
            result = self.op_callable(ctx.operator, ctx.owner, ctx.value)
        elif params_len == 4:
            result = self.op_callable(ctx.operator, ctx.owner, ctx.value, ctx)
        if result is None:
            return
        if result is True:
            return
        if result is False:
            raise ValidationException(
                keypath_messages={ctx.keypath_root: 'unauthorized operation'},
                root=ctx.root)
        if isinstance(result, str):
            raise ValidationException(
                keypath_messages={ctx.keypath_root: result},
                root=ctx.root)
        raise ValueError('invalid validator')
