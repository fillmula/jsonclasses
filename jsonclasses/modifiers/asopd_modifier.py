"""module for assigning operator directly modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING
from ..excs import ValidationException
from .modifier import Modifier
from ..fdef import Fdef
if TYPE_CHECKING:
    from ..ctx import Ctx


class AsopdModifier(Modifier):
    """Assigning operator directly modifier assigns the operator to the
    current field directly.
    """

    def define(self, fdef: Fdef) -> None:
        fdef._requires_operator_assign = True

    def validate(self, ctx: Ctx) -> None:
        if ctx.holder.is_new or ctx.keypathr[-1] in ctx.holder.modified_fields:
            if ctx.val is None:
                raise ValidationException(
                    keypath_messages={
                        '.'.join([str(k) for k in ctx.keypathr]): "no operator being assigned"},
                    root=ctx.root)
