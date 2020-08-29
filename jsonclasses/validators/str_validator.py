from ..exceptions import ValidationException
from .validator import Validator

class StrValidator(Validator):

  def validate(self, value, key_path, root, all_fields):
    if value is not None and type(value) is not str:
      raise ValidationException(
        { key_path: f'Value \'{value}\' at \'{key_path}\' should be str.' },
        root
      )
