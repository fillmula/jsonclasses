"""module for tostr modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class ToStrModifier(Modifier):
    """ToStr Modifier transforms value into a str"""

    def transform(self, ctx: Ctx) -> Any:
        is_int_or_float_or_bool = type(ctx.val) is int or type(ctx.val) is float or type(ctx.val) is bool
        return str(ctx.val) if is_int_or_float_or_bool else ctx.val
