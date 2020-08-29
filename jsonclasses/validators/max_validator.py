from typing import Union
from ..exceptions import ValidationException
from .validator import Validator

class MaxValidator(Validator):

  value: float

  def __init__(self, value):
    self.value = value

  def validate(self, value, key_path, root, all_fields):
    if value is not None and value > self.value:
      raise ValidationException(
        { key_path: f'Value \'{value}\' at \'{key_path}\' should not be greater than {self.value}.' },
        root
      )
