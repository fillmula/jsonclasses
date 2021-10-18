"""module for match modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING, Callable
from re import search
from ..excs import ValidationException
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class MatchModifier(Modifier):
    """Match modifier validates value against pattern."""

    def __init__(self, pattern: str | Callable | Types) -> None:
        self.pattern = pattern

    def validate(self, ctx: Ctx) -> None:
        pattern = self.resolve_param(self.pattern, ctx)
        if isinstance(ctx.val, str) and search(pattern, ctx.val) is None:
            ctx.raise_vexc(f'value does not match \'{pattern}\'')
