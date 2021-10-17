"""module for salt modifier."""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx

class SaltModifier(Modifier):
    """Salt modifier add salt to a string. This is mostly used for password."""

    def __init__(self) -> None:
        self.check_packages()

    def packages(self) -> dict[str, (str, str)] | None:
        return {'bcrypt': ('bcrypt', '>=3.2.0,<4.0.0')}

    def transform(self, ctx: Ctx) -> Any:
        from bcrypt import hashpw, gensalt
        if type(ctx.val) is str:
            return hashpw(ctx.val.encode(), gensalt()).decode('utf-8')
        return ctx.val
