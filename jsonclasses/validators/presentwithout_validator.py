"""module for required validator."""
from typing import Union
from ..exceptions import ValidationException
from .validator import Validator
from ..ctx import Ctx


class PresentWithoutValidator(Validator):
    """Fields marked with presentwithout validator are forced presented if
    referring field is not present. If referring field has None value, this
    field's value should be present. If referring field has non None value,
    value of this field is not forced to be present.
    """

    def __init__(self, referring_keys: Union[str, list[str]]) -> None:
        if isinstance(referring_keys, str):
            self.referring_keys = [referring_keys]
        else:
            self.referring_keys = referring_keys

    def validate(self, ctx: Ctx) -> None:
        if ctx.value is not None:
            return
        for key in self.referring_keys:
            try:
                referred_value = getattr(ctx.owner, key)
            except AttributeError:
                raise ValueError('Unexist referring key '
                                 f'\'{key}\' '
                                 'passed to present without validator.')
            if referred_value is not None:
                return
        if ctx.value is None:
            raise ValidationException(
                {ctx.keypath_root: (f'Value at \'{ctx.keypath_root}\''
                                        ' should be present since it\'s '
                                        'referring values are not '
                                        'presented.')},
                ctx.root)
