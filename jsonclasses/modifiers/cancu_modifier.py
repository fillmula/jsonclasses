"""module for canu modifier."""
from __future__ import annotations
from typing import Callable, TYPE_CHECKING
from inspect import signature
from .modifier import Modifier
from ..fdef import Fdef
from ..excs import ValidationException
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class CanCUModifier(Modifier):
    """Whether this operator can create or update on this field.
    """

    def __init__(self, checker: Callable | Types) -> None:
        self.checker = checker

    def validate(self, ctx: Ctx) -> None:
        if ctx.operator is None:
            ctx.raise_vexc('operator not present')
        if callable(self.checker):
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
                ctx.raise_vexc('operation is not permitted')
            if isinstance(result, str):
                ctx.raise_vexc(result)
            raise ValueError('invalid modifier')
        else:
            transformed = self.checker.modifier.transform(ctx)
            try:
                self.checker.modifier.validate(ctx.nval(transformed))
            except ValidationException:
                ctx.raise_vexc('operation is not permitted')
