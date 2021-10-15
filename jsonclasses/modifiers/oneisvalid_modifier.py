"""module for or modifier."""
from __future__ import annotations
from typing import Callable, TYPE_CHECKING
from inspect import signature
from ..excs import ValidationException
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types



class OneIsValidModifier(Modifier):
    """One is valid modifier validates with subroutines."""

    def __init__(self, subroutines: list[Callable | Types]) -> None:
        for item in subroutines:
            if callable(item):
                params_len = len(signature(item).parameters)
                if params_len > 2 or params_len < 1:
                    raise ValueError('not a valid or subroutine callable')
        self.subroutines = subroutines

    def validate(self, ctx: Ctx) -> None:
        for item in self.subroutines:
            from ..types import Types
            if isinstance(item, Types):
                tresult = item.modifier.transform(ctx)
                try:
                    item.modifier.validate(ctx.nval(tresult))
                    return
                except ValidationException:
                    continue
            else:
                params_len = len(signature(item).parameters)
                if params_len == 1:
                    result = callable(ctx.val)
                elif params_len == 2:
                    result = callable(ctx.val, ctx)
                if result is None:
                    return
                if result is True:
                    return
        ctx.raise_vexc('none is valid')
