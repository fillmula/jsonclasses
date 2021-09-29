"""module for authorization identity modifier."""
from __future__ import annotations
from typing import Callable, TYPE_CHECKING
from inspect import signature
from ..fdef import Fdef
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx
    from ..types import Types


class AuthByModifier(Modifier):
    """Fields marked with auth by are used for authorization.
    """

    def __init__(self, checker: Types) -> None:
        self.checker = checker

    def define(self, fdef: Fdef) -> None:
        fdef._auth_by = True
        fdef._auth_by_checker = self.checker
