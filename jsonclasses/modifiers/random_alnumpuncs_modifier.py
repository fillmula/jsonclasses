"""module for random alnumpuncs modifier."""
from __future__ import annotations
import random
from typing import Any, TYPE_CHECKING, Callable
from random import sample

from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class RandomAlnumpuncsModifier(Modifier):
    """Random alnumpuncs modifier generates random alnumpuncs as result."""

    def __init__(self, length: int | Callable | Types) -> None:
        self.length = length

    def transform(self, ctx: Ctx) -> Any:
        ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
        ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
        digits = '0123456789'
        ascii_letters = ascii_lowercase + ascii_uppercase
        return ''.join(sample(punctuation+ascii_letters+digits, self.resolve_param(self.length, ctx)))
