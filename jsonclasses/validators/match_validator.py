"""module for match validator."""
from __future__ import annotations
from typing import TYPE_CHECKING
from re import search
from ..excs import ValidationException
from .validator import Validator
if TYPE_CHECKING:
    from ..ctx import Ctx


class MatchValidator(Validator):
    """Match validator validates value against pattern."""

    def __init__(self, pattern: str) -> None:
        self.pattern = pattern

    def validate(self, ctx: Ctx) -> None:
        if ctx.val is None:
            return
        value = ctx.val
        if search(self.pattern, value) is None:
            kp = '.'.join([str(k) for k in ctx.keypathr])
            raise ValidationException(
                {kp: f'Value \'{value}\' at \'{kp}\' should match \'{self.pattern}\'.'},
                ctx.root
            )
