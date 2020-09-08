from typing import Any
from ..field import Field, CollectionNullability
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator

class NullableValidator(Validator):

  def define(self, field: Field):
    field.collection_nullability = CollectionNullability.NULLABLE

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    pass
