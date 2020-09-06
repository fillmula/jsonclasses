from typing import Any
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator

class StrValidator(Validator):

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool):
    if value is not None and type(value) is not str:
      raise ValidationException(
        { key_path: f'Value \'{value}\' at \'{key_path}\' should be str.' },
        root
      )
