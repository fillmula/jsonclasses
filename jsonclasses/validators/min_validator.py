from typing import Any
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator

class MinValidator(Validator):

  def __init__(self, min_value):
    self.min_value = min_value

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool):
    if value is not None and value < self.min_value:
      raise ValidationException(
        { key_path: f'Value \'{value}\' at \'{key_path}\' should not be less than {self.min_value}.' },
        root
      )
