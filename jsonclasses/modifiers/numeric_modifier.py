"""module for numeric modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING
from ..excs import ValidationException
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class NumericModifier(Modifier):
    """Numeric modifier raises if value is not a numeric."""

    def validate(self, ctx: Ctx) -> None:
        if isinstance(ctx.val, str) and not ctx.val.isnumeric():
            ctx.raise_vexc('value is not numeric string')

