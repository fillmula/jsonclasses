from typing import Any
from ..exceptions import ValidationException
from .validator import Validator

class NonnullValidator(Validator):

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool):
    pass

  def transform(self, value, camelize_keys: bool, key: str = ''):
    return {} if value is None else value
