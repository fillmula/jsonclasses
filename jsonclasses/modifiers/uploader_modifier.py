"""module for uploader modifier."""
from __future__ import annotations
from typing import Callable, Any, TYPE_CHECKING
from inspect import signature
from .modifier import Modifier
from ..uploaders import request_uploader
if TYPE_CHECKING:
    from ..ctx import Ctx


class UploaderModifier(Modifier):
    """Upload file stream to cloud storage and get the string url back."""

    def __init__(self, arg: str | Callable) -> None:
        self.arg = arg
        if callable(arg):
            params_len = len(signature(arg).parameters)
            if params_len > 2 or params_len < 1:
                raise ValueError('not a valid transformer')

    def transform(self, ctx: Ctx) -> Any:
        if ctx.val is None:
            return None
        if callable(self.arg):
            params_len = len(signature(self.arg).parameters)
            if params_len == 1:
                return self.arg(ctx.val)
            elif params_len == 2:
                return self.arg(ctx.val, ctx)
        else:
            uploader = request_uploader(self.arg)
            return uploader.upload(ctx.val)
