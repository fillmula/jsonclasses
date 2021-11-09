"""module for hexcolor modifier."""
from __future__ import annotations
from typing import Any, cast, TYPE_CHECKING
from re import compile, match
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


hex_color_regex = compile('[0-9a-fA-F]{6}')

class HexColorModifier(Modifier):
    """Email modifier raises if value is not valid email."""

    def transform(self, ctx: Ctx) -> Any:
        if type(ctx.val) is str:
            strval = cast(str, ctx.val)
            if strval.startswith('#'):
                return strval[1:]
        return ctx.val

    def validate(self, ctx: Ctx) -> None:
        if isinstance(ctx.val, str) and match(hex_color_regex, ctx.val) is None:
            ctx.raise_vexc('value is not hex color string')