from typing import Callable, Any
from inspect import signature
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator

class ValidateValidator(Validator):

  def __init__(self, validate_callable: Callable):
    self.validate_callable = validate_callable

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool):
    params_len = len(signature(self.validate_callable).parameters)
    if params_len == 1:
      result = self.validate_callable(value)
    elif params_len == 2:
      result = self.validate_callable(value, key_path)
    else:
      result = self.validate_callable(value, key_path, root)
    if result is not None:
      raise ValidationException(keypath_messages={ key_path: result }, root=root)
