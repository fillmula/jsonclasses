"""module for match modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING
from re import search
from ..excs import ValidationException
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class MatchModifier(Modifier):
    """Match modifier validates value against pattern."""

    def __init__(self, pattern: str) -> None:
        self.pattern = pattern

    def validate(self, ctx: Ctx) -> None:
        if isinstance(ctx.val, str) and search(self.pattern, ctx.val) is None:
            ctx.raise_vexc(f'value does not match \'{self.pattern}\'')
