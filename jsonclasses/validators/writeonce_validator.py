from typing import Any
from ..field_description import FieldDescription, WriteRule
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator

class WriteonceValidator(Validator):

  def define(self, field_description: FieldDescription):
    field_description.write_rule = WriteRule.WRITE_ONCE

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    pass
