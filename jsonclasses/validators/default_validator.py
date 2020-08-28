from typing import Any
from ..exceptions import ValidationException
from .validator import Validator

class DefaultValidator(Validator):

  value: Any

  def __init__(self, value):
    self.value = value

  def validate(self, value, key_path, root, all):
    pass

  def transform(self, value):
    return self.value if value is None else value
