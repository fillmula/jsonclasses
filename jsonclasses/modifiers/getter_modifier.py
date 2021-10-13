from __future__ import annotations
from typing import TYPE_CHECKING, Callable
from inspect import signature
from ..fdef import FStore, Fdef
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class GetterModifier(Modifier):
    """Getter modifier marks a field as calculated field. It's not stored."""

    def __init__(self, calc: Callable | Types) -> None:
        from ..types import Types
        self.calc = calc
        if not isinstance(calc, Types):
            if not callable(calc):
                raise ValueError('getter is not callable')
            params_len = len(signature(calc).parameters)
            if params_len != 1:
                raise ValueError('not a valid getter')

    def define(self, fdef: Fdef) -> None:
        fdef._fstore = FStore.CALCULATED
        fdef._getter = self.calc
