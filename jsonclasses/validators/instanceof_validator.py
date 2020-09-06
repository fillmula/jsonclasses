from typing import Dict, Any
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator
from ..utils import default_validator_for_type, keypath
from inflection import underscore, camelize

class InstanceOfValidator(Validator):

  def __init__(self, json_object_class):
    # is JSONObject
    if hasattr(json_object_class, '_set'):
      self.json_object_class = json_object_class
    # in the future, handle string argument
    else:
      raise ValueError('argument passed to InstanceOfValidator should be subclass of JSONObject.')

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool):
    if value is None:
      return
    value.validate(base_key=key_path, root=root, all_fields=all_fields)

  def transform(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    if value is None:
      return None
    if type(value) is not dict:
      return value
    return self.json_object_class(**value)

  def tojson(self, value, config: Config):
    if value is None:
      return None
    return value.tojson()
