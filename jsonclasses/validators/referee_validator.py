from typing import Any
from ..field_description import FieldDescription
from ..config import Config
from .validator import Validator

class RefereeValidator(Validator):

  def __init__(self, referee_key: str) -> None:
    self.referee_key = referee_key

  def define(self, field_description: FieldDescription) -> None:
    field_description.join_table_referee_key = self.referee_key

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> None:
    pass
