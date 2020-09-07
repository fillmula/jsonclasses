from typing import Any
from ..config import Config
from .validator import Validator

class LinkedByValidator(Validator):

  def __init__(self, foreign_key: str):
    self.foreign_key = foreign_key

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    pass
