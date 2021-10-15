"""module for isprefixof modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class IsPrefixOfModifier(Modifier):
    """Has prefix modifier for checking if a str is suffix of another str."""

    def __init__(self, prefix: str | list[Any]) -> None:
        self.prefix = prefix

    def validate(self, ctx: Ctx) -> None:
        if isinstance(ctx.val, list):
            if not self.prefix[:len(ctx.val)] == ctx.val:
                ctx.raise_vexc('prefix is not found')
        if type(ctx.val) is str:
            if not self.prefix.startswith(ctx.val):
                ctx.raise_vexc('prefix is not found')
