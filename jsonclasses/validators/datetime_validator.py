from typing import Any
from datetime import datetime
from ..field_description import FieldDescription, FieldType
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator
from ..reference_map import referenced

@referenced
class DatetimeValidator(Validator):

  def define(self, field_description: FieldDescription):
    field_description.field_type = FieldType.DATETIME

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    if value is not None and type(value) is not datetime:
      raise ValidationException(
        { key_path: f'Value \'{value}\' at \'{key_path}\' should be datetime.' },
        root
      )

  def transform(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    if value is None:
      return None
    elif type(value) is str:
      return datetime.fromisoformat(value.replace('Z', ''))
    else:
      return value

  def tojson(self, value: Any, config: Config):
    if value is not None:
      return value.isoformat()[:23] + 'Z'
