from typing import Union
from ..exceptions import ValidationException
from .validator import Validator

class MaxlengthValidator(Validator):

  def __init__(self, maxlength: int):
    self.maxlength = maxlength

  def validate(self, value, key_path, root, all_fields):
    if value is not None and len(value) > self.maxlength:
      raise ValidationException(
        { key_path: f'Value \'{value}\' at \'{key_path}\' should have length not greater than {self.maxlength}.' },
        root
      )
