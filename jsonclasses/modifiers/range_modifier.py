"""module for range modifier."""
from __future__ import annotations
from typing import Union, TYPE_CHECKING
from .modifier import Modifier
from .min_modifier import MinModifier
from .max_modifier import MaxModifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class RangeModifier(Modifier):
    """A range modifier validates value against a range."""

    def __init__(self, min: Union[int, float], max: Union[int, float]):
        self.min = min
        self.max = max

    def validate(self, ctx: Ctx) -> None:
        if ctx.val is None:
            return
        MinModifier(self.min).validate(ctx)
        MaxModifier(self.max).validate(ctx)
