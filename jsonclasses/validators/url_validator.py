"""module for match validator."""
from re import compile, match, IGNORECASE
from ..exceptions import ValidationException
from .validator import Validator
from ..contexts import ValidatingContext


class UrlValidator(Validator):
    """URL validator raises if value is not valid url."""

    def validate(self, context: ValidatingContext) -> None:
        if context.value is None:
            return
        value = context.value
        # https://stackoverflow.com/questions/7160737/how-to-validate-a-url-in-python-malformed-or-not
        regex = compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', IGNORECASE)
        if match(regex, value) is None:
            kp = context.keypath_root
            raise ValidationException(
                {kp: f'Value \'{value}\' at \'{kp}\' is not valid url.'},
                context.root
            )
