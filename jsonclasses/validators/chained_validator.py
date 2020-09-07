from typing import List, Dict, Any
from functools import reduce
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator
from ..utils.eager_validator_index_after_index import eager_validator_index_after_index
from ..utils.last_eager_validator_index import last_eager_validator_index
from ..utils.reference_map import referenced

@referenced
class ChainedValidator(Validator):

  def __init__(self, validators: List[Validator] = []):
    self.validators = validators

  def append(self, *args: Validator):
    return ChainedValidator([*self.validators, *args])

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    if root == None:
      root = value
    keypath_messages: Dict[str, str] = {}
    start_validator_index = last_eager_validator_index(self.validators)
    for validator in self.validators[start_validator_index:]:
      try:
        validator.validate(value, key_path, root, all_fields, config)
      except ValidationException as exception:
        keypath_messages.update(exception.keypath_messages)
        if not all_fields:
          break
    if len(keypath_messages) > 0:
      raise ValidationException(keypath_messages, root)

  def _validate_and_transform(
    self,
    validator: Validator,
    value: Any,
    key_path: str,
    root: Any,
    all_fields: bool,
    config: Config
  ) -> Any:
    validator.validate(value, key_path, root, all_fields, config)
    return validator.transform(value, key_path, root, all_fields, config)

  def transform(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    curvalue = value
    index = 0
    next_index = eager_validator_index_after_index(self.validators, index)
    while next_index is not None:
      validators = self.validators[index:next_index]
      curvalue = reduce(lambda v, validator: self._validate_and_transform(validator, v, key_path, root, all_fields, config), validators, curvalue)
      index = next_index + 1
      next_index = eager_validator_index_after_index(self.validators, index)
    curvalue = reduce(lambda v, validator: validator.transform(v, key_path, root, all_fields, config), self.validators[index:], curvalue)
    return curvalue

  def tojson(self, value: Any, config: Config):
    return reduce(lambda v, validator: validator.tojson(v, config), self.validators, value)
