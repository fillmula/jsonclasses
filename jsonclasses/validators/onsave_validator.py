"""module for onsave validator."""
from typing import Callable, Any
from inspect import signature
from .validator import Validator
from ..contexts import TransformingContext


class OnSaveValidator(Validator):
    """On save validator is called when saving is triggered."""

    def __init__(self, callback: Callable) -> None:
        self.callback = callback

    def serialize(self, context: TransformingContext) -> Any:
        params_len = len(signature(self.callback).parameters)
        if params_len == 0:
            self.callback()
        elif params_len == 1:
            self.callback(context.value)
        else:
            raise ValueError('wrong number of arguments provided to onsave '
                             'validator.')
        return context.value
