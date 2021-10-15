"""module for canr modifier."""
from __future__ import annotations
from typing import Callable, TYPE_CHECKING
from .modifier import Modifier
from ..fdef import Fdef
if TYPE_CHECKING:
    from ..types import Types


class CanRModifier(Modifier):
    """Whether this operator can read on this field.
    """

    def __init__(self, checker: Callable | Types) -> None:
        self.checker = checker
