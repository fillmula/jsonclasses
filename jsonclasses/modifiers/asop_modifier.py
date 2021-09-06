"""module for assigning operator modifier."""
from __future__ import annotations
from typing import Callable, TYPE_CHECKING
from inspect import signature
from ..fdef import Fdef
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class AsopModifier(Modifier):
    """Assigning operator modifier assigns the transfromed operator to the
    current field.
    """

    def __init__(self, transformer: Callable) -> None:
        if not callable(transformer):
            raise ValueError('asop transformer is not callable')
        params_len = len(signature(transformer).parameters)
        if params_len > 3 or params_len < 1:
            raise ValueError('not a valid asop transformer')
        self.transformer = transformer

    def define(self, fdef: Fdef) -> None:
        fdef._requires_operator_assign = True
        fdef._operator_assign_transformer = self.transformer

    def validate(self, ctx: Ctx) -> None:
        if ctx.holder.is_new or ctx.keypathr[-1] in ctx.holder.modified_fields:
            if ctx.val is None:
                ctx.raise_vexc('no operator being assigned')
