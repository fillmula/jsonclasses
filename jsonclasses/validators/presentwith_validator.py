"""module for required validator."""
from ..exceptions import ValidationException
from .validator import Validator
from ..contexts import ValidatingContext


class PresentWithValidator(Validator):
    """Fields marked with presentwith validator are forced presented if
    referring field is present. If referring field has None value, this field's
    value is optional. If referring field has non None value, value of this
    field is required.
    """

    def __init__(self, referring_key: str) -> None:
        self.referring_key = referring_key

    def validate(self, context: ValidatingContext) -> None:
        if context.value is not None:
            return
        try:
            referred_value = getattr(context.owner, self.referring_key)
        except AttributeError:
            raise ValueError(f'Unexist referring key \'{self.referring_key}\' '
                             'passed to present with validator.')
        if referred_value is not None and context.value is None:
            raise ValidationException(
                {context.keypath_root: (f'Value at \'{context.keypath_root}\''
                                        ' should be present since it\'s '
                                        'referring value is presented.')},
                context.root)
