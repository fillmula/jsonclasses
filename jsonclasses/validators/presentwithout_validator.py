"""module for required validator."""
from typing import Union
from ..exceptions import ValidationException
from .validator import Validator
from ..contexts import ValidatingContext


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

    def validate(self, context: ValidatingContext) -> None:
        if context.value is not None:
            return
        for key in self.referring_keys:
            try:
                referred_value = getattr(context.owner, key)
            except AttributeError:
                raise ValueError('Unexist referring key '
                                 f'\'{key}\' '
                                 'passed to present without validator.')
            if referred_value is not None:
                return
        if context.value is None:
            raise ValidationException(
                {context.keypath_root: (f'Value at \'{context.keypath_root}\''
                                        ' should be present since it\'s '
                                        'referring values are not '
                                        'presented.')},
                context.root)
