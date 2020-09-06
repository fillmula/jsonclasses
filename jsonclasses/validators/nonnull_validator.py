from typing import Any
from ..exceptions import ValidationException
from .validator import Validator

class NonnullValidator(Validator):

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool):
    pass

  def transform(self, value: Any, key_path: str, root: Any, all_fields: bool, camelize_keys: bool):
    return {} if value is None else value
