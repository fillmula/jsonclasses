"""module for digit modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING
from ..excs import ValidationException
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class DigitModifier(Modifier):
    """Digit modifier raises if value is not a digit."""

    def validate(self, ctx: Ctx) -> None:
        if isinstance(ctx.val, str) and not ctx.val.isdigit():
            ctx.raise_vexc('value is not digit string')
