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
        if ctx.val is None:
            return
        value = ctx.val
        if search(self.pattern, value) is None:
            kp = '.'.join([str(k) for k in ctx.keypathr])
            raise ValidationException(
                {kp: f'value does not match \'{self.pattern}\''},
                ctx.root
            )
