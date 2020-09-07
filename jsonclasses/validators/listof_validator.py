from __future__ import annotations
from typing import Any
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator
from .required_validator import RequiredValidator
from ..utils.default_validator_for_type import default_validator_for_type
from ..utils.keypath import keypath
from ..utils.is_nullable_type import is_nullable_type
from ..utils.reference_map import referenced, resolve_class

@referenced
class ListOfValidator(Validator):

  def __init__(self, types: Any):
    self.types = types

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    if value is None:
      return
    if type(value) is not list:
      raise ValidationException(
        { key_path: f'Value \'{value}\' at \'{key_path}\' should be a list.' },
        root
      )
    validator = None
    if isinstance(self.types, resolve_class('Types')):
      validator = self.types.validator
    else:
      validator = default_validator_for_type(self.types, graph_sibling=config.linked_class)
    if validator:
      if not is_nullable_type(validator):
        validator = validator.append(RequiredValidator())
      keypath_messages = {}
      for i, v in enumerate(value):
        try:
          validator.validate(v, keypath(key_path, i), root, all_fields, config)
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
    if type(value) is not list:
      return value
    if isinstance(self.types, resolve_class('Types')):
      validator = self.types.validator
    else:
      validator = default_validator_for_type(self.types, graph_sibling=config.linked_class)
    if validator:
      return [ validator.transform(v, keypath(key_path, i), root, all_fields, config) for i, v in enumerate(value) ]
    else:
      return value

  def tojson(self, value: Any, config: Config):
    if value is None:
      return None
    if type(value) is not list:
      return value
    if isinstance(self.types, resolve_class('Types')):
      validator = self.types.validator
    else:
      validator = default_validator_for_type(self.types, graph_sibling=config.linked_class)
    if validator:
      return [ validator.tojson(v, config) for v in value ]
    else:
      return value
