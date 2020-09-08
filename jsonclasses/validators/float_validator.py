from typing import Any
from ..field import Field, FieldType
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator
from ..utils.reference_map import referenced

@referenced
class FloatValidator(Validator):

  def define(self, field: Field):
    field.field_type = FieldType.FLOAT

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    if value is not None and type(value) is not float:
      raise ValidationException(
        { key_path: f'Value \'{value}\' at \'{key_path}\' should be float.' },
        root
      )

  def transform(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    if value is None:
      return None
    elif type(value) is int:
      return float(value)
    else:
      return value
