from __future__ import annotations
from typing import Any, Callable, TYPE_CHECKING
from inspect import signature
from ..fdef import FStore, Fdef
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class AssignModifier(Modifier):
    """Assign modifier assigns value to the current object."""

    def __init__(self, name: str, val: Any | Callable | Types) -> None:
        self.name = name
        self.val = val
        if callable(val):
            params_len = len(signature(val).parameters)
            if params_len != 0:
                raise ValueError('not a valid assigner')

    def transform(self, ctx: Ctx) -> Any:
        from ..types import Types
        if callable(self.val):
            setattr(ctx.val, self.name, self.val())
            return ctx.val
        if isinstance(self.val, Types):
            setattr(ctx.val, self.name, self.val.modifier.transform(ctx))
            return ctx.val
        setattr(ctx.val, self.name, self.val)
        return ctx.val
