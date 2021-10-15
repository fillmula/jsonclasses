"""module for hasprefix modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class HasprefixModifier(Modifier):
    """Hasprefix modifier for checking if a str is suffix of another str."""

    def __init__(self, affix: str) -> None:
        self.affix = affix

    def validate(self, ctx: Ctx) -> None:
        if ctx.val is None:
            return
        if type(ctx.val) is str:
            return ctx.val.startswith(self.affix)
        else:
            return ctx.val
