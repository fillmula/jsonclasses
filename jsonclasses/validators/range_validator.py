from typing import Any
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator
from .min_validator import MinValidator
from .max_validator import MaxValidator

class RangeValidator(Validator):

  def __init__(self, min_value, max_value):
    self.min_value = min_value
    self.max_value = max_value

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool):
    if value is not None:
      MinValidator(self.min_value).validate(value, key_path, root, all_fields)
      MaxValidator(self.max_value).validate(value, key_path, root, all_fields)
