from typing import Any
from ..exceptions import ValidationException
from .validator import Validator

class DefaultValidator(Validator):

  default_value: Any

  def __init__(self, default_value):
    self.default_value = default_value

  def validate(self, value, key_path, root, all_fields):
    pass

  def transform(self, value):
    if hasattr(self.default_value, '__call__'):
      return self.default_value() if value is None else value
    else:
      return self.default_value if value is None else value
