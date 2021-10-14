"""module for random int modifier."""
from __future__ import annotations
from random import randrange
from typing import Any, TYPE_CHECKING, Union
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class RandomIntModifier(Modifier):
    """Random int modifier generates random int as result."""

    def __init__(self, min_value: Union[int, float], max_value: Union[int, float]) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def transform(self, ctx: Ctx) -> Any:
        if self.min_value < self.max_value:
            return randrange(self.min_value, self.max_value)
        else:
            message = f'{self.min_value} is not less than or equal {self.max_value}'
        ctx.raise_vexc(message)
