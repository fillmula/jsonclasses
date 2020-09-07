from typing import Any
from ..config import Config
from .validator import Validator

class LinkToValidator(Validator):

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    pass
