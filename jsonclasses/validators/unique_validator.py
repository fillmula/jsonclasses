from typing import Any
from ..field_description import FieldDescription, FieldType
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator

class UniqueValidator(Validator):

  def define(self, field_description: FieldDescription):
    field_description.unique = True

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    pass
