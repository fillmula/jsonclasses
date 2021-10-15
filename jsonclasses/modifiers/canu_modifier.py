"""module for canu modifier."""
from __future__ import annotations
from typing import Callable, TYPE_CHECKING
from .cancu_modifier import CanCUModifier
from ..fdef import Fdef
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class CanUModifier(CanCUModifier):
    """Whether this operator can update on this field.
    """

    def validate(self, ctx: Ctx) -> None:
        if not ctx.owner.is_new:
            super().validate(ctx)
