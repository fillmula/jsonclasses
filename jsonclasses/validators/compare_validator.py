"""module for compare validator."""
from typing import Callable, cast, TYPE_CHECKING
from inspect import signature
from ..exceptions import ValidationException
from .validator import Validator
if TYPE_CHECKING:
    from ..ctx import Ctx


class CompareValidator(Validator):
    """Compare validator validates field value by compare old and new values.
    """

    def __init__(self, compare_callable: Callable) -> None:
        if not callable(compare_callable):
            raise ValueError('compare argument is not callable')
        params_len = len(signature(compare_callable).parameters)
        if params_len < 2 or params_len > 3:
            raise ValueError('not a valid compare callable')
        self.compare_callable = compare_callable

    def validate(self, ctx: Ctx) -> None:
        from ..jobject import JObject
        name = ctx.keypathp[-1]
        parent = cast(JObject, ctx.parent)
        if name not in parent.previous_values:
            return
        prev_value = parent.previous_values[name]
        params_len = len(signature(self.compare_callable).parameters)
        if params_len == 2:
            result = self.compare_callable(prev_value, ctx.val)
        elif params_len == 3:
            result = self.compare_callable(prev_value, ctx.val, ctx)
        if result is True:
            return
        if result is False:
            raise ValidationException(
                keypath_messages={ctx.keypath_root: 'compare failed'},
                root=ctx.root)
        if result is not None:
            raise ValidationException(
                keypath_messages={ctx.keypath_root: result},
                root=ctx.root)
