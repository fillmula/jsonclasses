"""module for random float modifier."""
from __future__ import annotations
from random import uniform
from typing import Any, TYPE_CHECKING, Union
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class RandomFloatModifier(Modifier):
    """Random float modifier generates random float as result."""

    def __init__(self, min_value: Union[int, float], max_value: Union[int, float]) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def transform(self, ctx: Ctx) -> Any:
        return uniform(self.min_value, self.max_value)
