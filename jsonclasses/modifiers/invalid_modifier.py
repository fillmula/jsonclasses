"""module for modifier modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING
from ..excs import ValidationException
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class InvalidModifier(Modifier):
    """A modifier that turns value into invalid."""

    def validate(self, ctx: Ctx) -> None:
        """Raises invalid exception."""
        ctx.raise_vexc('value is invalid')
