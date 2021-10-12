"""module for cross fetch modifier."""
from __future__ import annotations
from typing import Optional, Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class CrossFetchModifier(Modifier):
    """Fetch a class with value matches this object's value.
    """

    def __init__(self,
                 cls_name: str,
                 this_key: str,
                 that_key: Optional[str] = None) -> None:
        self.cls_name = cls_name
        self.this_key = this_key
        self.that_key = that_key if that_key is not None else this_key

    def transform(self, ctx: Ctx) -> Any:
        parent = ctx.parent
        that_cls = parent.__class__.cdef.jconf.cgraph.fetch(self.cls_name).cls
        that_val = getattr(parent, self.this_key)
        that_obj = that_cls.one(**{self.that_key: that_val}).optional.exec()
        if that_obj is None:
            ctx.raise_vexc('cross fetch failed')
        return that_obj
