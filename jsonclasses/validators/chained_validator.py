from typing import List, Dict
from functools import reduce
from ..exceptions import ValidationException
from .validator import Validator

class ChainedValidator(Validator):

  validators: List[Validator] = []

  def __init__(self, validators: List[Validator] = []):
    self.validators = validators

  def append(self, validator: Validator):
    return ChainedValidator([*self.validators, validator])

  def validate(self, value, key_path = '', root = None, all = True):
    if root == None:
      root = value
    keypath_messages: Dict[str, str] = {}
    for validator in self.validators:
      try:
        validator.validate(value, key_path, root)
      except ValidationException as exception:
        keypath_messages.update(exception.keypath_messages)
        if not all:
          break
    if keypath_messages.__len__ > 0:
      raise ValidationException(keypath_messages, root)

  def transform(self, value):
    return reduce(lambda value, validator: validator.transform(value), self.validators, value)

  def to_json(self, value):
    return reduce(lambda value, validator: validator.to_json(value), self.validators, value)
