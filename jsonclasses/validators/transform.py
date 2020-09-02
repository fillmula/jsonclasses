from typing import Callable
from ..exceptions import ValidationException
from .validator import Validator

class TransformValidator(Validator):

  def __init__(self, transformer: Callable):
    self.transformer = transformer

  def validate(self, value, key_path, root, all_fields):
    pass

  def transform(self, value):
    if value is not None:
      return self.transformer(value)
    else:
      return None
