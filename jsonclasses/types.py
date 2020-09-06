from __future__ import annotations
from typing import List, Dict, Union, Callable, Any, Optional
from datetime import date, datetime
from .utils.reference_map import referenced
from .validators import *

@referenced
class Types:
  '''The class of types marks object. Types marks provide necessary information
  about an json object's shape, transformation, validation, serialization and
  sanitization.
  '''

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
  def internal(self):
    '''Fields marked with internal will not be accepted as input, and it will
    not be present in output. These fields are internal and hidden from users.
    '''
    return Types(self.validator.append(ReadonlyValidator(), WriteonlyValidator()))

  @property
  def index(self):
    '''Fields marked with index are picked up by ORM integrations to setup
    database column index for you. This marker doesn't have any effect around
    transforming and validating.
    '''
    return Types(self.validator.append(IndexValidator()))

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
    return Types(self.validator.append(UniqueValidator()))

  @property
  def str(self):
    '''Fields marked with str should be str type. This is a type marker.
    '''
    return Types(self.validator.append(StrValidator()))

  def match(self, pattern: str):
    '''Fields marked with match are tested againest the argument regular
    expression pattern.
    '''
    return Types(self.validator.append(MatchValidator(pattern)))

  def oneof(self, str_list):
    '''This is the enum equivalent for jsonclasses. Values in the provided list
    are considered valid values.
    '''
    return Types(self.validator.append(OneOfValidator(str_list)))

  def minlength(self, length: int):
    '''Values at fields marked with minlength should have a length which is not
    less than length.

    Args:
      length (): The minimum length required for the value.

    Returns:
      Types: A new types chained with this marker.
    '''
    return Types(self.validator.append(MinlengthValidator(length)))

  def maxlength(self, length: int):
    '''Values at fields marked with maxlength should have a length which is not
    greater than length.

    Args:
      length (int): The minimum length required for the value.

    Returns:
      Types: A new types chained with this marker.
    '''
    return Types(self.validator.append(MaxlengthValidator(length)))

  def length(self, minlength: int, maxlength: Optional[int] = None):
    '''
    '''
    return Types(self.validator.append(LengthValidator(minlength, maxlength)))

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

  def listof(self, types: Any):
    '''Fields marked with listof should be a list of the given type. This is a
    type marker.
    '''
    return Types(self.validator.append(ListOfValidator(types)))

  def dictof(self, types: Any):
    '''Fields marked with listof should be a str keyed dict of the given type.
    This is a type marker.
    '''
    return Types(self.validator.append(DictOfValidator(types)))

  def shape(self, types):
    '''Fields marked with shape are objects shaped with given shape. This is a
    type marker.
    '''
    return Types(self.validator.append(ShapeValidator(types)))

  def instanceof(self, json_object_class):
    '''Fields marked with instance of are objects of given class.
    '''
    return Types(self.validator.append(InstanceOfValidator(json_object_class)))

  @property
  def required(self):
    '''Fields marked with required are invalid when value is not presented aka
    None.

    Returns:
      Types: A new types chained with this marker.
    '''
    return Types(self.validator.append(RequiredValidator()))

  @property
  def nullable(self):
    '''Fields marked with nullable can be None. This is the default behavior
    even without this marker. It's the opposite to required marker. Values
    inside lists have implicitly required marker. Use this to allow null or
    None values inside lists.

    Returns:
      Types: A new types chained with this marker.
    '''
    return Types(self.validator.append(NullableValidator()))

  def validate(self, validate_callable):
    '''The validate field mark takes a validator callable as its sole argument.
    Use this to define custom field value validations.

    Args:
      validate_callable (Callable): The validate callable tasks 3 arguments,
      value, key_path, and root. Returning None means the value is valid, while
      returning a str message means the validation failed.

    Returns:
      Types: A new types chained with this marker.
    '''
    return Types(self.validator.append(ValidateValidator(validate_callable)))

  # transformers

  def default(self, value: Any):
    '''During initialization, if values of fields with default are not provided.
    The default value is used instead of leaving blank.

    Args:
      value (any): The default value of this field. If the value is callable,
      it's return value is used.

    Returns:
      Types: A new types chained with this marker.
    '''
    return Types(self.validator.append(DefaultValidator(value)))

  def truncate(self, max_length: int):
    '''During initialization and set, if string value is too long, it's
    truncated to argument max length.

    Args:
      max_length (int): The allowed max length of the field value.

    Returns:
      Types: A new types chained with this marker.
    '''
    return Types(self.validator.append(TruncateValidator(max_length)))

  def transform(self, transformer: Callable):
    '''This mark applies transfromer on the value. When value is None, the
    transformer is not called. This class barely means to transform. Use
    default mark with a callable to assign calculated default value.

    Args:
      transformer (Callable): This transformer function takes one argument which
      is the current value of the field.

    Returns:
      Types: A new types chained with this marker.
    '''
    return Types(self.validator.append(EagerValidator(), TransformValidator(transformer)))

  @property
  def nonnull(self):
    '''This marker is a instructional transformer designated for shape. This is
    not a validator. To mark a field is required and should not be null, use
    `required` instead. This transformer should be used right before shape, to
    given shape an instruction of not leaving null for the shaped field.

    Returns:
      Types: A new types chained with this marker.
    '''
    return Types(self.validator.append(NonnullValidator()))

types = Types()
'''The root of the types marker. To mark an field with type annotation,
accessor annotation, validator annotation and transformer annotation, use types
like this:

  @jsonclass
  class MyObject(JSONObject):
    my_field_one: bool = types.bool.readonly.required
    my_field_two: password = types.bool.writeonly.length(8, 16).transform(salt).required
'''
