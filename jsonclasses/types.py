from typing import List, Dict, Union
from datetime import date, datetime
from .validators import *

class Types:

  validator: ChainedValidator

  def __init__(self, validator: ChainedValidator = ChainedValidator()):
    self.validator = validator

  # chained validators

  @property
  def invalid(self):
    return Types(self.validator.append(Validator()))

  @property
  def readonly(self):
    '''Fields marked with readonly will not be able to go through
    initialization and set method. You can update value of these fields
    directly or through update method. This prevents client side to post data
    directly into these fields.
    '''
    return Types(self.validator.append(ReadonlyValidator()))

  @property
  def writeonly(self):
    '''Fields marked with writeonly will not be available in outgoing json form.
    Users' password is a great example of writeonly.
    '''
    return Types(self.validator.append(WriteonlyValidator()))

  @property
  def readwrite(self):
    '''Fields marked with readwrite will be presented in both inputs and outputs.
    This is the default behavior. And this specifier can be omitted.
    '''
    return Types(self.validator.append(ReadwriteValidator()))

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
