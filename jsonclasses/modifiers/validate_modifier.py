"""module for validate modifier."""
from __future__ import annotations
from typing import Callable, TYPE_CHECKING
from inspect import signature
from ..excs import ValidationException
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class ValidateModifier(Modifier):
    """Validate modifier takes a modifier."""

    def __init__(self, validate_callable: Callable) -> None:
        if not callable(validate_callable):
            raise ValueError('modifier is not callable')
        params_len = len(signature(validate_callable).parameters)
        if params_len > 2 or params_len < 1:
            raise ValueError('not a valid modifier')
        self.validate_callable = validate_callable

    def validate(self, ctx: Ctx) -> None:
        if ctx.val is None:
            return
        params_len = len(signature(self.validate_callable).parameters)
        if params_len == 1:
            result = self.validate_callable(ctx.val)
        elif params_len == 2:
            result = self.validate_callable(ctx.val, ctx)
        if result is None:
            return
        if result is True:
            return
        if result is False:
            ctx.raise_vexc('invalid value')
        if isinstance(result, str):
            ctx.raise_vexc(result)
        raise ValueError('invalid modifier')
