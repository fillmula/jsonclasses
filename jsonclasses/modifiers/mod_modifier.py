"""module for mod modifier."""
from __future__ import annotations
from typing import Any, Union, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx

class ModModifier(Modifier):
    """Mod modifier mods number value."""

    def __init__(self, a_number: Union[int, float]):
        self.a_number = a_number

    def transform(self, ctx: Ctx) -> Any:
        return ctx.val % self.a_number if type(ctx.val) is int or type(ctx.val) is float else ctx.val
