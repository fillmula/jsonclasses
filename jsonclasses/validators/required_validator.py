from typing import Any
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator

class RequiredValidator(Validator):

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    if value is None:
      raise ValidationException(
        { key_path: f'Value at \'{key_path}\' should not be None.' },
        root
      )
