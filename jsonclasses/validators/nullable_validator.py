from typing import Any
from ..field_description import FieldDescription, CollectionNullability
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator

class NullableValidator(Validator):

  def define(self, field_description: FieldDescription):
    field_description.collection_nullability = CollectionNullability.NULLABLE

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    pass
