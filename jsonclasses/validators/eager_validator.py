from typing import Any
from .validator import Validator
from ..field import Field, FieldType
from ..config import Config

class EagerValidator(Validator):
  '''An EagerValidator marks fields for initialization and set stage validation.
  This is used usually before heavy transforming validators.
  '''

  def define(self, field: Field):
    field.has_eager_validator = True

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    pass
