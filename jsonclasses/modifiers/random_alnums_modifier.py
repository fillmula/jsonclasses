"""module for random alnums modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING, Callable
from random import sample
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class RandomAlnumsModifier(Modifier):
    """Random alnums modifier generates random alnums as result."""

    def __init__(self, length: int | Callable | Types) -> None:
        self.length = length

    def transform(self, ctx: Ctx) -> Any:
        ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
        ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        digits = '0123456789'
        ascii_letters = ascii_lowercase + ascii_uppercase
        return ''.join(sample(ascii_letters+digits, self.resolve_param(self.length, ctx)))
