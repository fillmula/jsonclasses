"""module for passin modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class PassinModifier(Modifier):
    """Passin modifier uses passin value as the result."""

    def transform(self, ctx: Ctx) -> Any:
        return ctx.passin
