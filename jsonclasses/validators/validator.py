from typing import Any
from ..config import Config
from ..exceptions import ValidationException

class Validator:

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool):
    raise ValidationException(
      { key_path: f'Value \'{value}\' at \'{key_path}\' is invalid.' },
      root
    )

  def transform(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    return value

  def tojson(self, value, config: Config):
    return value
