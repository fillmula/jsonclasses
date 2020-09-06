from typing import Callable, Any
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator

class TransformValidator(Validator):

  def __init__(self, transformer: Callable):
    self.transformer = transformer

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool):
    pass

  def transform(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    if value is not None:
      return self.transformer(value)
    else:
      return None
