from typing import List, Dict, Any
from functools import reduce
from ..exceptions import ValidationException
from .validator import Validator

class ChainedValidator(Validator):

  def __init__(self, validators: List[Validator] = []):
    self.validators = validators

  def append(self, *args: Validator):
    return ChainedValidator([*self.validators, *args])

  def validate(self, value, key_path = '', root = None, all_fields = True):
    if root == None:
      root = value
    keypath_messages: Dict[str, str] = {}
    for validator in self.validators:
      try:
        validator.validate(value, key_path, root, all_fields)
      except ValidationException as exception:
        keypath_messages.update(exception.keypath_messages)
        if not all_fields:
          break
    if len(keypath_messages) > 0:
      raise ValidationException(keypath_messages, root)

  def transform(self, value):
    # if not eager_validate:
    return reduce(lambda v, validator: validator.transform(v), self.validators, value)
    # else:
    #   curvalue = value
    #   index = 0
    #   next_index = eager_validator_index_after_index(self.validators, index)
    #   while True:
    #     validators = self.validators[index:next_index]
    #     curvalue = reduce(lambda v, validator: self.__validate_and_transform(validator, v), validators, curvalue)
    #     if next_index is None:
    #       break
    #     else:
    #       index = next_index
    #       next_index = eager_validator_index_after_index(self.validators, index)
    #   return reduce(lambda v, validator: validator.transform(v), self.validators[index:], curvalue)

  def tojson(self, value):
    return reduce(lambda v, validator: validator.tojson(v), self.validators, value)

  def __validate_and_transform(self, validator: Validator, value: Any):
    validator.validate(value)
    return validator.transform(value)
