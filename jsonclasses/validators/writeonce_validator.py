from typing import Any
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator

class WriteonceValidator(Validator):

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    pass
