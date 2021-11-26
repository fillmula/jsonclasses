"""module for fval modifier."""
from __future__ import annotations
from typing import Any, Callable, cast, TYPE_CHECKING
from ..objref import ObjRef
from ..jobject import JObject
from ..fdef import FStore
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class FValModifier(Modifier):
    """Get value at field from a JSONClass object.
    """

    def __init__(self, field_name: str | Callable | Types) -> None:
        self.field_name = field_name

    def transform(self, ctx: Ctx) -> Any:
        if ctx.val is None:
            return None
        field_name = self.resolve_param(self.field_name, ctx)
        val = cast(JObject, ctx.val)
        field = val.__class__.cdef.field_named(field_name)
        obj = getattr(val, field_name)
        if field.fdef.fstore == FStore.LOCAL_KEY:
            if obj is not None:
                return obj
            else:
                kt = val.__class__.cdef.jconf.ref_name_strategy
                fidname = kt(field)
                cls_name = field.fdef.inst_cls.__name__
                ref_id = getattr(val, fidname)
                if ref_id is None:
                    return None
                else:
                    return ObjRef(cls=cls_name, id=ref_id)
        else:
            return obj
