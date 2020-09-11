from typing import Callable, Any
from ..field_description import FieldDescription, FieldType
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator

class TransformValidator(Validator):

  def __init__(self, transformer: Callable) -> None:
    self.transformer = transformer

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> None:
    pass

  def transform(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> Any:
    if value is not None:
      return self.transformer(value)
    else:
      return None
