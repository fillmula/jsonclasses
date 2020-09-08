from typing import Any
from ..field_description import FieldDescription, ReadRule
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator

class WriteonlyValidator(Validator):

  def define(self, field_description: FieldDescription):
    field_description.read_rule = ReadRule.NO_READ

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    pass
