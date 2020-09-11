from __future__ import annotations
from typing import Any
from ..field_description import FieldDescription, FieldType
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator

class StrValidator(Validator):

  def define(self, field_description: FieldDescription) -> None:
    field_description.field_type = FieldType.STR

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> None:
    if value is not None and type(value) is not str:
      raise ValidationException(
        { key_path: f'Value \'{value}\' at \'{key_path}\' should be str.' },
        root
      )
