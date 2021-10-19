"""module for hassuffix modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING, Callable
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class IsSuffixOfModifier(Modifier):
    """Has suffix modifier for checking if a str is suffix of another str."""

    def __init__(self, is_suffix: str | list[Any] | Callable | Types) -> None:
        self.is_suffix = is_suffix

    def validate(self, ctx: Ctx) -> None:
        if isinstance(ctx.val, list):
            if not self.resolve_param(self.is_suffix, ctx)[-len(ctx.val):] == ctx.val:
                ctx.raise_vexc('suffix is not found')
        elif type(ctx.val) is str:
            if not self.resolve_param(self.suffix, ctx).endswith(ctx.val):
                ctx.raise_vexc('suffix is not found')
