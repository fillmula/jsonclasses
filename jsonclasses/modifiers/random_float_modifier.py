"""module for random float modifier."""
from __future__ import annotations
from random import uniform
from typing import Any, TYPE_CHECKING, Callable, Union
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class RandomFloatModifier(Modifier):
    """Random float modifier generates random float as result."""

    def __init__(self, min_value: int | float | Callable | Types,
                 max_value: int | float | Callable | Types) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def transform(self, ctx: Ctx) -> Any:
        min_value = self.resolve_param(self.min_value, ctx)
        max_value = self.resolve_param(self.max_value, ctx)
        return uniform(min_value, max_value)
