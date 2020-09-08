from typing import Any
from ..field_description import FieldDescription
from ..field_description import FieldDescription, FieldType
from ..config import Config
from ..exceptions import ValidationException

class Validator:

  def define(self, field_description: FieldDescription):
    pass

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    raise ValidationException(
      { key_path: f'Value \'{value}\' at \'{key_path}\' is invalid.' },
      root
    )

  def transform(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    return value

  def tojson(self, value: Any, config: Config):
    return value
