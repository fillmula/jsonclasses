from typing import Any
from ..field_description import FieldDescription, FieldType
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator
from ..reference_map import referenced

@referenced
class BoolValidator(Validator):

  def define(self, field_description: FieldDescription):
    field_description.field_type = FieldType.BOOL

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    if value is not None and type(value) is not float:
      raise ValidationException(
        { key_path: f'Value \'{value}\' at \'{key_path}\' should be bool.' },
        root
      )
