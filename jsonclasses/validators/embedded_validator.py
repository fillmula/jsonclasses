from typing import Any
from ..field import Field, FieldStorage
from ..config import Config
from .validator import Validator

class EmbeddedValidator(Validator):

  def define(self, field: Field):
    field.field_storage = FieldStorage.EMBEDDED

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    pass
