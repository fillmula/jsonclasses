from typing import List, Dict, Union
from datetime import date, datetime
from .validators import *

class Types:

  validator: ChainedValidator

  def __init__(self, validator: ChainedValidator = ChainedValidator()):
    self.validator = validator

  # def __infer_python_type_from_validator(self):
  #   validators = self.validator.validators
  #   if len(validators) > 0:
  #     validator = validators[0]
  #     validator_type = type(validator)
  #     if validator_type is StrValidator:
  #       return str
  #     elif validator_type is BoolValidator:
  #       return bool
  #     elif validator_type is IntValidator:
  #       return int
  #     elif validator_type is FloatValidator:
  #       return float
  #     elif validator_type is DateValidator:
  #       return date
  #     elif validator_type is DatetimeValidator:
  #       return datetime

  # chained validators

  @property
  def invalid(self):
    return Types(self.validator.append(Validator()))

  @property
  def str(self):
    return Types(self.validator.append(StrValidator()))

  def match(self, pattern):
    return Types(self.validator.append(MatchValidator(pattern)))

  def one_of(self, str_list):
    return Types(self.validator.append(OneOfValidator(str_list)))

  @property
  def int(self):
    return Types(self.validator.append(IntValidator()))

  @property
  def float(self):
    return Types(self.validator.append(FloatValidator()))

  def min(self, value: float):
    return Types(self.validator.append(MinValidator(value)))

  def max(self, value: float):
    return Types(self.validator.append(MaxValidator(value)))

  def range(self, min_value: float, max_value: float):
    return Types(self.validator.append(RangeValidator(min_value, max_value)))

  @property
  def bool(self):
    return Types(self.validator.append(BoolValidator()))

  @property
  def date(self):
    return Types(self.validator.append(DateValidator()))

  @property
  def datetime(self):
    return Types(self.validator.append(DatetimeValidator()))

  # @property
  # def list_of(self, types: Types):
  #   return Types(self.validator.append(ListOfValidator(types)))

  @property
  def required(self):
    return Types(self.validator.append(RequiredValidator()))

  # transformers

  def default(self, value):
    return Types(self.validator.append(DefaultValidator(value)))

  def truncate(self, max_length):
    return Types(self.validator.append(TruncateValidator(max_length)))

types = Types()
