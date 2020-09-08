from typing import Any
from ..field import Field, FieldType
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator

class IndexValidator(Validator):

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    pass
