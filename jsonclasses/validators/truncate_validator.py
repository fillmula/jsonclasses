from typing import Any
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator

class TruncateValidator(Validator):

  def __init__(self, max_length):
    self.max_length = max_length

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool):
    pass

  def transform(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    if value is not None and value.__len__() > self.max_length:
      return value[:self.max_length]
    else:
      return value
