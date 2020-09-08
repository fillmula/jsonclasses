from typing import Any
from ..field_description import FieldDescription, FieldStorage
from ..config import Config
from .validator import Validator

class EmbeddedValidator(Validator):

  def define(self, field_description: FieldDescription):
    field_description.field_storage = FieldStorage.EMBEDDED

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    pass
