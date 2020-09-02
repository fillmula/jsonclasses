from typing import Union
from ..exceptions import ValidationException
from .validator import Validator

class MinlengthValidator(Validator):

  value: int

  def __init__(self, value: int):
    self.value = value

  def validate(self, value, key_path, root, all_fields):
    if value is not None and len(value) < self.value:
      raise ValidationException(
        { key_path: f'Value \'{value}\' at \'{key_path}\' should have length not less than {self.value}.' },
        root
      )
