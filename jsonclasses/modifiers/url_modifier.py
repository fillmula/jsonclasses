"""module for match modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING
from re import compile, match, IGNORECASE
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


# https://stackoverflow.com/questions/7160737/how-to-validate-a-url-in-python-malformed-or-not
url_regex = compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', IGNORECASE)

class UrlModifier(Modifier):
    """URL modifier raises if value is not valid url."""

    def validate(self, ctx: Ctx) -> None:
        if isinstance(ctx.val, str) and match(url_regex, ctx.val) is None:
            ctx.raise_vexc('value is not valid url string')
