"""module for hasprefix modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class HasPrefixModifier(Modifier):
    """Has prefix modifier for checking if a str is suffix of another str."""

    def __init__(self, prefix: str | list[Any]) -> None:
        self.prefix = prefix

    def validate(self, ctx: Ctx) -> None:
        if isinstance(ctx.val, list):
            if not ctx.val[:len(ctx.val)] == self.prefix:
                ctx.raise_vexc('prefix is not found')
        if type(ctx.val) is str:
            if not ctx.val.startswith(self.prefix):
                ctx.raise_vexc('prefix is not found')
