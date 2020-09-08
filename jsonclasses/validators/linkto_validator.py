from typing import Any
from ..field import Field, FieldStorage
from ..config import Config
from .validator import Validator

class LinkToValidator(Validator):

  def define(self, field: Field):
    field.field_storage = FieldStorage.LOCAL_KEY

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    pass
