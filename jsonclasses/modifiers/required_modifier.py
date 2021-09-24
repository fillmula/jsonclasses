"""module for required modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING
from ..fdef import Fdef
from .modifier import Modifier
from ..fdef import FStore
from ..jconf import JConf
from ..isjsonclass import isjsonobject
if TYPE_CHECKING:
    from ..ctx import Ctx


class RequiredModifier(Modifier):
    """Mark a field as required."""

    def define(self, fdef: Fdef) -> None:
        fdef._required = True

    def validate(self, ctx: Ctx) -> None:
        storage = FStore.EMBEDDED
        if ctx.fdef is not None:
            storage = ctx.fdef.fstore
        if storage == FStore.FOREIGN_KEY:  # we don't check foreign key
            return
        if storage == FStore.LOCAL_KEY:
            if ctx.val is None:  # check key presence
                jconf: JConf = ctx.holder.__class__.cdef.jconf
                ko = str(ctx.keypathh[0])
                field = ctx.holder.__class__.cdef.field_named(ko)
                local_key = jconf.ref_key_encoding_strategy(field)
                if isinstance(ctx.holder, dict):
                    if ctx.holder.get(local_key) is None:
                        ctx.raise_vexc('value required')
                elif isjsonobject(ctx.holder):
                    try:
                        local_key_value = getattr(ctx.holder, local_key)
                    except AttributeError:
                        ctx.raise_vexc('value required')
                    if local_key_value is None:
                        ctx.raise_vexc('value required')
            return
        if ctx.val is None:
            ctx.raise_vexc('value required')
