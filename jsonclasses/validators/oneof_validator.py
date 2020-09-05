# OneOfValidator
from typing import List
from ..exceptions import ValidationException
from .validator import Validator

class OneOfValidator(Validator):

  def __init__(self, str_list: List[str]):
    self.str_list = str_list

  def validate(self, value, key_path, root, all_fields):
    if value is not None and value not in self.str_list:
      raise ValidationException(
        { key_path: f'Value \'{value}\' at \'{key_path}\' should be one of \'{self.str_list}\'.' },
        root
      )
