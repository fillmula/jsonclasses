"""module for fobj modifier."""
from __future__ import annotations
from typing import Any, Callable, cast, TYPE_CHECKING
from ..jobject import JObject
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class FObjModifier(Modifier):
    """Get object at field from a JSONClass object. If the object is not exist,
    include it and return it.
    """

    def __init__(self, field_name: str | Callable | Types) -> None:
        self.field_name = field_name

    def transform(self, ctx: Ctx) -> Any:
        if ctx.val is None:
            return None
        field_name = self.resolve_param(self.field_name, ctx)
        val = cast(JObject, ctx.val)
        if getattr(val, field_name) is None:
            val.include(field_name)
        return getattr(val, field_name)
