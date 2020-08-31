from ..exceptions import ValidationException
from .validator import Validator

class FloatValidator(Validator):

  def validate(self, value, key_path, root, all_fields):
    if value is not None and type(value) is not float:
      raise ValidationException(
        { key_path: f'Value \'{value}\' at \'{key_path}\' should be float.' },
        root
      )

  def transform(self, value):
    if value is None:
      return None
    elif type(value) is int:
      return float(value)
    else:
      return value
