from typing import Any
from ..field import Field, WriteRule, ReadRule
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator

class ReadwriteValidator(Validator):

  def define(self, field: Field):
    field.write_rule = WriteRule.UNLIMITED
    field.read_rule = ReadRule.UNLIMITED

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    pass
