from typing import Any
from ..exceptions import ValidationException
from .validator import Validator

class DefaultValidator(Validator):

  def __init__(self, default_value: Any):
    self.default_value = default_value

  def validate(self, value, key_path, root, all_fields):
    pass

  def transform(self, value: Any):
    if value is None:
      if callable(self.default_value):
        return self.default_value()
      else:
        return self.default_value
    else:
      return value
