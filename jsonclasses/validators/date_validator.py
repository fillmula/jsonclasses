from typing import Any
from datetime import date
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator

class DateValidator(Validator):

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool):
    if value is not None and type(value) is not date:
      raise ValidationException(
        { key_path: f'Value \'{value}\' at \'{key_path}\' should be date.' },
        root
      )

  def transform(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    if value is None:
      return None
    elif type(value) is str:
      return date.fromisoformat(value[:10])
    else:
      return value

  def tojson(self, value, config: Config):
    if value is not None:
      return value.isoformat() + 'T00:00:00.000Z'
