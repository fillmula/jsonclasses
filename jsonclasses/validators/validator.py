from typing import Any
from ..exceptions import ValidationException

class Validator:

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool):
    raise ValidationException(
      { key_path: f'Value \'{value}\' at \'{key_path}\' is invalid.' },
      root
    )

  def transform(self, value, camelize_keys: bool, key: str = ''):
    return value

  def tojson(self, value, camelize_keys: bool):
    return value
