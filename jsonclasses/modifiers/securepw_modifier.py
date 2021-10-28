"""module for securepw modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from re import compile, VERBOSE, search
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx

securepw_regex = compile(r'''(
    ^(?=.*[A-Z])
    (?=.*[!@#$&*`~()\-_+=\[\]{}:;'",<>.?\\|/])
    (?=.*[0-9])
    (?=.*[a-z])
    .*$
    )''', VERBOSE)

class SecurepwModifier(Modifier):
    """Securepw modifier checks password is secure."""

    def validate(self, ctx: Ctx) -> None:
        if isinstance(ctx.val, str) and search(securepw_regex, ctx.val) is None:
            ctx.raise_vexc('value is not secure password')
