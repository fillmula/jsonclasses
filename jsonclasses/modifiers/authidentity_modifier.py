"""module for authorization identity modifier."""
from __future__ import annotations
from typing import Callable, TYPE_CHECKING
from inspect import signature
from ..fdef import Fdef
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class AuthIdentityModifier(Modifier):
    """Fields marked with authidentity are used for authorization.
    """

    def define(self, fdef: Fdef) -> None:
        fdef._auth_identity = True
