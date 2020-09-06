from typing import Any
from ..exceptions import ValidationException
from .validator import Validator

class ReadonlyValidator(Validator):

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool):
    pass
