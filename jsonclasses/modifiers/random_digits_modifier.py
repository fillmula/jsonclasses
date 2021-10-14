"""module for random digits modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from random import sample
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class RandomDigitsModifier(Modifier):
    """Random digits modifier generates random digits as result."""

    def __init__(self, length: int) -> None:
        self.length = length

    def transform(self, ctx: Ctx) -> Any:
        digits = '0123456789'
        return ''.join(sample(digits, self.length))
