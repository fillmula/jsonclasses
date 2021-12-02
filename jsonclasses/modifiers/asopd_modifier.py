"""module for assigning operator directly modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING
from .modifier import Modifier
from ..fdef import FDef
if TYPE_CHECKING:
    from ..ctx import Ctx


class AsopdModifier(Modifier):
    """Assigning operator directly modifier assigns the operator to the
    current field directly.
    """

    def define(self, fdef: FDef) -> None:
        fdef._requires_operator_assign = True

    def validate(self, ctx: Ctx) -> None:
        if ctx.holder.is_new or ctx.keypathr[-1] in ctx.holder.modified_fields:
            field = ctx.holder.__class__.cdef.field_named(ctx.keypathr[-1])
            fidname = ctx.holder.__class__.cdef.jconf.ref_name_strategy(field)
            if getattr(ctx.holder, fidname) is None:
                ctx.raise_vexc('no operator being assigned')
