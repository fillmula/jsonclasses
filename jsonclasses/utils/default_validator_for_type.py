from datetime import date, datetime
from .reference_map import resolve_class

def default_validator_for_type(type):
  '''This function returns the default synthesized validator for given Python
  type.

  Args:
    type (Union[str, int, float, bool, date, datetime]): A python type.

  Returns:
    Validator: A synthesized validator for the given Python type or None if it
    can't be synthesized.
  '''
  ChainedValidator = resolve_class('ChainedValidator')
  if type is str:
    StrValidator = resolve_class('StrValidator')
    return ChainedValidator().append(StrValidator())
  elif type is float:
    FloatValidator = resolve_class('FloatValidator')
    return ChainedValidator().append(FloatValidator())
  elif type is int:
    IntValidator = resolve_class('IntValidator')
    return ChainedValidator().append(IntValidator())
  elif type is bool:
    BoolValidator = resolve_class('BoolValidator')
    return ChainedValidator().append(BoolValidator())
  elif type is date:
    DateValidator = resolve_class('DateValidator')
    return ChainedValidator().append(DateValidator())
  elif type is datetime:
    DatetimeValidator = resolve_class('DatetimeValidator')
    return ChainedValidator().append(DatetimeValidator())
  else:
    return None
