"""module for range modifier."""
from __future__ import annotations
from typing import Callable, Union, TYPE_CHECKING
from .modifier import Modifier
from .min_modifier import MinModifier
from .max_modifier import MaxModifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class RangeModifier(Modifier):
    """A range modifier validates value against a range."""

    def __init__(self, min: int | float | Callable | Types, max: int | float | Callable | Types):
        self.min = min
        self.max = max

    def validate(self, ctx: Ctx) -> None:
        if ctx.val is None:
            return
        MinModifier(self.resolve_param(self.min, ctx)).validate(ctx)
        MaxModifier(self.resolve_param(self.max, ctx)).validate(ctx)
