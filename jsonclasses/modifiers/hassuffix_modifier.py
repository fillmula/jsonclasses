"""module for hassuffix modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class HasSuffixModifier(Modifier):
    """Has suffix modifier for checking if a str is suffix of another str"""

    def __init__(self, suffix: str | list[Any]) -> None:
        self.suffix = suffix

    def validate(self, ctx: Ctx) -> None:
        if isinstance(ctx.val, list):
            if not ctx.val[-len(self.suffix):] == self.suffix:
                ctx.raise_vexc('suffix is not found')
        if type(ctx.val) is str:
            if not ctx.val.endswith(self.suffix):
                ctx.raise_vexc('suffix is not found')
