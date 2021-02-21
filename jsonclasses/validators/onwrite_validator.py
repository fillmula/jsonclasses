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
        self.callback = callback

    def serialize(self, context: TransformingContext) -> Any:
        from ..orm_object import ORMObject
        name = context.keypath_parent
        parent = cast(ORMObject, context.parent)
        if not parent.is_new and name not in parent.modified_fields:
            return
        params_len = len(signature(self.callback).parameters)
        if params_len == 0:
            self.callback()
        elif params_len == 1:
            self.callback(context.value)
        else:
            raise ValueError('wrong number of arguments provided to onwrite '
                             'validator.')
        return context.value
