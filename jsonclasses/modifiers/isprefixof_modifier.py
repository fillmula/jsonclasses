"""module for isprefixof modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING, Callable
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class IsPrefixOfModifier(Modifier):
    """Has prefix modifier for checking if a str is suffix of another str."""

    def __init__(self, prefix: str | list[Any] | Callable | Types) -> None:
        self.prefix = prefix

    def validate(self, ctx: Ctx) -> None:
        if isinstance(ctx.val, list):
            if not self.resolve_param(self.prefix, ctx)[:len(ctx.val)] == ctx.val:
                ctx.raise_vexc('prefix is not found')
        elif type(ctx.val) is str:
            if not self.resolve_param(self.prefix, ctx).startswith(ctx.val):
                ctx.raise_vexc('prefix is not found')
