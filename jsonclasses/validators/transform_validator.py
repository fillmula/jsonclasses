from typing import Callable, Any
from ..exceptions import ValidationException
from .validator import Validator

class TransformValidator(Validator):

  def __init__(self, transformer: Callable):
    self.transformer = transformer

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool):
    pass

  def transform(self, value, camelize_keys: bool, key: str = ''):
    if value is not None:
      return self.transformer(value)
    else:
      return None
