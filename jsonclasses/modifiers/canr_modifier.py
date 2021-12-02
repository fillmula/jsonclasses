"""module for canr modifier."""
from __future__ import annotations
from typing import Callable, Any, TYPE_CHECKING
from inspect import signature
from .modifier import Modifier
from ..fdef import FDef
from ..excs import ValidationException
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class CanRModifier(Modifier):
    """Whether this operator can read on this field.
    """

    def __init__(self, checker: Callable | Types) -> None:
        self.checker = checker

    def tojson(self, ctx: Ctx) -> Any:
        super().tojson(ctx)
        if ctx.operator is None:
            return None
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
                return ctx.val
            if result is True:
                return ctx.val
            if result is False:
                return None
            if isinstance(result, str):
                return None
            raise ValueError('invalid modifier')
        else:
            transformed = self.checker.modifier.transform(ctx)
            try:
                self.checker.modifier.validate(ctx.nval(transformed))
                return ctx.val
            except ValidationException:
                return None
