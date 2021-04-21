"""module for onsave validator."""
from typing import Callable, Any, cast
from inspect import signature
from .validator import Validator
from ..contexts import TransformingContext


class OnWriteValidator(Validator):
    """On write validator is called when field has a new value and saving is
    triggered.
    """

    def __init__(self, callback: Callable) -> None:
        if not callable(callback):
            raise ValueError('onwrite callback is not callable')
        params_len = len(signature(callback).parameters)
        if params_len > 2:
            raise ValueError('not a valid onwrite callback')
        self.callback = callback

    def serialize(self, context: TransformingContext) -> Any:
        from ..jsonclass_object import JSONClassObject
        name = context.keypath_parent
        parent = cast(JSONClassObject, context.parent)
        if not parent.is_new and name not in parent.modified_fields:
            return context.value
        params_len = len(signature(self.callback).parameters)
        if params_len == 0:
            self.callback()
        elif params_len == 1:
            self.callback(context.value)
        elif params_len == 2:
            self.callback(context.value, context)
        return context.value
