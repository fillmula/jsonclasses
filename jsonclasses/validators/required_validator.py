from ..exceptions import ValidationException
from .validator import Validator

class RequiredValidator(Validator):

  def validate(self, value, key_path, root, all_fields):
    if value is None:
      raise ValidationException(
        { key_path: f'Value at \'{key_path}\' should not be None.' },
        root
      )
