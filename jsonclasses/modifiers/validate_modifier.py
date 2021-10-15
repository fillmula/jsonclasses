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

    def __init__(self, validator: Callable) -> None:
        if callable(validator):
            params_len = len(signature(validator).parameters)
            if params_len > 2 or params_len < 1:
                raise ValueError('not a valid modifier')
        self.validator = validator

    def validate(self, ctx: Ctx) -> None:
        from ..types import Types
        if isinstance(self.validator, Types):
            tresult = self.validator.modifier.transform(ctx)
            try:
                self.validator.modifier.validate(ctx.nval(tresult))
                return
            except ValidationException:
                ctx.raise_vexc('invalid value')
        if ctx.val is None:
            return
        params_len = len(signature(self.validator).parameters)
        if params_len == 1:
            result = self.validator(ctx.val)
        elif params_len == 2:
            result = self.validator(ctx.val, ctx)
        if result is None:
            return
        if result is True:
            return
        if result is False:
            ctx.raise_vexc('invalid value')
        if isinstance(result, str):
            ctx.raise_vexc(result)
