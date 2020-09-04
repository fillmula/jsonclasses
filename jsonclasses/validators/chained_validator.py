from typing import List, Dict, Any
from functools import reduce
from ..exceptions import ValidationException
from .validator import Validator

class ChainedValidator(Validator):

  def __init__(self, validators: List[Validator] = []):
    self.validators = validators

  def append(self, *args: Validator):
    return ChainedValidator([*self.validators, *args])

  def validate(
    self,
    value,
    key_path = '',
    root = None,
    all_fields = True,
    start_validator_index: int = 0
  ):
    if root == None:
      root = value
    keypath_messages: Dict[str, str] = {}
    for validator in self.validators[start_validator_index:]:
      try:
        validator.validate(value, key_path, root, all_fields)
      except ValidationException as exception:
        keypath_messages.update(exception.keypath_messages)
        if not all_fields:
          break
    if len(keypath_messages) > 0:
      raise ValidationException(keypath_messages, root)

  def transform(self, value, camelize_keys: bool):
    return reduce(lambda v, validator: validator.transform(v, camelize_keys), self.validators, value)

  def tojson(self, value, camelize_keys: bool):
    return reduce(lambda v, validator: validator.tojson(v, camelize_keys), self.validators, value)
