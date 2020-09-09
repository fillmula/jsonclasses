from __future__ import annotations
from typing import Any
from ..field_description import FieldDescription, FieldType
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator
from .required_validator import RequiredValidator
from ..utils.keypath import keypath
from ..reference_map import referenced, resolve_class
from ..utils.nonnull_note import NonnullNote
from ..fields import collection_argument_type_to_types
from ..field_description import CollectionNullability

@referenced
class ListOfValidator(Validator):

  def __init__(self, types: Any):
    self.types = types

  def define(self, field_description: FieldDescription):
    field_description.field_type = FieldType.LIST

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    if value is None:
      return
    if type(value) is not list:
      raise ValidationException(
        { key_path: f'Value \'{value}\' at \'{key_path}\' should be a list.' },
        root
      )
    types = collection_argument_type_to_types(self.types, config.linked_class)
    if types:
      if types.field_description.collection_nullability == CollectionNullability.UNDEFINED:
        types = types.required
      keypath_messages = {}
      for i, v in enumerate(value):
        try:
          types.validator.validate(v, keypath(key_path, i), root, all_fields, config)
        except ValidationException as exception:
          if all_fields:
            keypath_messages.update(exception.keypath_messages)
          else:
            raise exception
      if len(keypath_messages) > 0:
        raise ValidationException(keypath_messages=keypath_messages, root=root)

  def transform(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    if value is None:
      return None
    elif isinstance(value, NonnullNote):
      value = []
    elif type(value) is not list:
      return value
    types = collection_argument_type_to_types(self.types, config.linked_class)
    if types:
      return [ types.validator.transform(v, keypath(key_path, i), root, all_fields, config) for i, v in enumerate(value) ]
    else:
      return value

  def tojson(self, value: Any, config: Config):
    if value is None:
      return None
    if type(value) is not list:
      return value
    types = collection_argument_type_to_types(self.types, config.linked_class)
    if types:
      return [ types.validator.tojson(v, config) for v in value ]
    else:
      return value
