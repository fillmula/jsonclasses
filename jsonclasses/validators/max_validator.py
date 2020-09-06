from typing import Any
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator

class MaxValidator(Validator):

  def __init__(self, max_value):
    self.max_value = max_value

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool):
    if value is not None and value > self.max_value:
      raise ValidationException(
        { key_path: f'Value \'{value}\' at \'{key_path}\' should not be greater than {self.max_value}.' },
        root
      )
