"""module for isobjof modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..jobject import JObject

class IsObjOfModifier(Modifier):
    """Value if value is object of class."""

    def __init__(self, cls: type[JObject] | str) -> None:
        self.cls = cls

    def validate(self, ctx: Ctx) -> None:
        if ctx.val is None:
            ctx.raise_vexc('none is not object of a class')
        if type(self.cls) is str:
            self.cls = ctx.owner.__class__.cdef.jconf.cgraph.fetch(self.cls).cls
        if not isinstance(ctx.val, self.cls):
            ctx.raise_vexc(f'value is not instance of {self.cls.__name__}')
