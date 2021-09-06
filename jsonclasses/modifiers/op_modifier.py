"""module for operator modifier."""
from __future__ import annotations
from typing import Callable, TYPE_CHECKING
from inspect import signature
from ..excs import ValidationException
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class OpModifier(Modifier):
    """Op modifier validates with user defined modifier."""

    def __init__(self, op_callable: Callable) -> None:
        if not callable(op_callable):
            raise ValueError('op modifier is not callable')
        params_len = len(signature(op_callable).parameters)
        if params_len > 4 or params_len < 1:
            raise ValueError('not a valid op modifier')
        self.op_callable = op_callable

    def validate(self, ctx: Ctx) -> None:
        if ctx.operator is None:
            ctx.raise_vexc('operator not present')
        params_len = len(signature(self.op_callable).parameters)
        if params_len == 1:
            result = self.op_callable(ctx.operator)
        elif params_len == 2:
            result = self.op_callable(ctx.operator, ctx.owner)
        elif params_len == 3:
            result = self.op_callable(ctx.operator, ctx.owner, ctx.val)
        elif params_len == 4:
            result = self.op_callable(ctx.operator, ctx.owner, ctx.val, ctx)
        if result is None:
            return
        if result is True:
            return
        if result is False:
            ctx.raise_vexc('unauthorized operation')
        if isinstance(result, str):
            ctx.raise_vexc(result)
        raise ValueError('invalid modifier')
