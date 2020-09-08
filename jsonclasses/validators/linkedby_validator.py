from typing import Any
from ..field_description import FieldDescription, FieldStorage
from ..config import Config
from .validator import Validator

class LinkedByValidator(Validator):

  def __init__(self, foreign_key: str):
    self.foreign_key = foreign_key

  def define(self, field_description: FieldDescription):
    field_description.field_storage = FieldStorage.FOREIGN_KEY
    field_description.foreign_key = self.foreign_key

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    pass
