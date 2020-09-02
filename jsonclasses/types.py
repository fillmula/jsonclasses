from typing import List, Dict, Union
from datetime import date, datetime
from .validators import *

class Types:
  '''The class of types marks object. Types marks provide necessary information
  about an json object's shape, transformation, validation, serialization and
  sanitization.
  '''

  validator: ChainedValidator

  def __init__(self, validator: ChainedValidator = ChainedValidator()):
    self.validator = validator

  @property
  def invalid(self):
    '''Fields marked with invalid will never be valid, thus these fields
    will never pass validation.
    '''
    return Types(self.validator.append(Validator()))

  @property
  def readonly(self):
    '''Fields marked with readonly will not be able to go through
    initialization and set method. You can update value of these fields
    directly or through update method. This prevents client side to post data
    directly into these fields.

    Readonly and writeonce cannot be presented together.
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
  def writeonce(self):
    '''Fields marked with writeonce can only be set once through initialization
    and set method. You can update value of these fields directly or through
    update method. This is suitable for e.g. dating app user gender. Gender
    should not be changed once set.

    Writeonce and readonly cannot be presented together.
    '''
    return Types(self.validator.append(WriteonceValidator()))

  @property
  def index(self):
    '''Fields marked with index are picked up by ORM integrations to setup
    database column index for you. This marker doesn't have any effect around
    transforming and validating.
    '''
    return Types(self.validator.append(IndexValidator))

  @property
  def unique(self):
    '''Fields marked with unique are picked up by ORM integrations to setup
    database column unique index for you. This marker doesn't have any effect
    around transforming and validating. When database engine raises an
    exception, jsonclasses's web framework integration will catch it and return
    400 automatically.

    If you are implementing jsonclasses ORM integration, you should use
    UniqueFieldException provided by jsonclasses.exceptions to keep consistency
    with other jsonclasses integrations.
    '''
    return Types(self.validator.append(UniqueValidator))

  @property
  def str(self):
    '''Fields marked with str should be str type. This is a type marker.
    '''
    return Types(self.validator.append(StrValidator()))

  def match(self, pattern):
    '''Fields marked with match are tested againest the argument regular
    expression pattern.
    '''
    return Types(self.validator.append(MatchValidator(pattern)))

  def one_of(self, str_list):
    '''This is the enum equivalent for jsonclasses. Values in the provided list
    are considered valid values.
    '''
    return Types(self.validator.append(OneOfValidator(str_list)))

  def minlength(self, length):
    '''Values at fields marked with minlength should have a length which is not
    less than length.

    Args:
      length (int): The minimum length required for the value.

    Returns:
      Types: A new types chained with this marker.
    '''
    return Types(self.validator.append(MinlengthValidator(length)))

  def maxlength(self, length):
    '''Values at fields marked with maxlength should have a length which is not
    greater than length.

    Args:
      length (int): The minimum length required for the value.

    Returns:
      Types: A new types chained with this marker.
    '''
    return Types(self.validator.append(MaxlengthValidator(length)))


  @property
  def int(self):
    '''Fields marked with int should be int type. This is a type marker.
    '''
    return Types(self.validator.append(IntValidator()))

  @property
  def float(self):
    '''Fields marked with float should be float type. This is a type marker.
    '''
    return Types(self.validator.append(FloatValidator()))

  def min(self, value: float):
    '''Fields marked with min are tested again this value. Values less than
    the argument value are considered invalid.
    '''
    return Types(self.validator.append(MinValidator(value)))

  def max(self, value: float):
    '''Fields marked with max are tested again this value. Values greater than
    the argument value are considered invalid.
    '''
    return Types(self.validator.append(MaxValidator(value)))

  def range(self, min_value: float, max_value: float):
    '''Fields marked with range are tested again argument values. Only values
    between the arguments range are considered valid.
    '''
    return Types(self.validator.append(RangeValidator(min_value, max_value)))

  @property
  def bool(self):
    '''Fields marked with bool should be bool type. This is a type marker.
    '''
    return Types(self.validator.append(BoolValidator()))

  @property
  def date(self):
    '''Fields marked with date should be date type. This is a type marker.
    '''
    return Types(self.validator.append(DateValidator()))

  @property
  def datetime(self):
    '''Fields marked with datetime should be datetime type. This is a type
    marker.
    '''
    return Types(self.validator.append(DatetimeValidator()))

  # @property
  # def list_of(self, types: Types):
  #   return Types(self.validator.append(ListOfValidator(types)))

  @property
  def required(self):
    '''Fields marked with required are invalid when value is not presented aka
    None.

    Returns:
      Types: A new types chained with this marker.
    '''
    return Types(self.validator.append(RequiredValidator()))

  # transformers

  def default(self, value):
    '''During initialization, if values of fields with default are not provided.
    The default value is used instead of leaving blank.

    Args:
      value (any): The default value of this field. If the value is callable,
      it's return value is used.

    Returns:
      Types: A new types chained with this marker.
    '''
    return Types(self.validator.append(DefaultValidator(value)))

  def truncate(self, max_length):
    '''During initialization and set, if string value is too long, it's
    truncated to argument max length.

    Args:
      max_length (int): The allowed max length of the field value.

    Returns:
      Types: A new types chained with this marker.
    '''
    return Types(self.validator.append(TruncateValidator(max_length)))

types = Types()
