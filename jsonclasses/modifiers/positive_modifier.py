"""module for positive modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING
from ..excs import ValidationException
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class PositiveModifier(Modifier):
    """Positive modifier marks value valid for large than zero."""

    def validate(self, ctx: Ctx) -> None:
        is_number = type(ctx.val) is int or type(ctx.val) is float
        if is_number and ctx.val <= 0:
            ctx.raise_vexc('value is not positive')
