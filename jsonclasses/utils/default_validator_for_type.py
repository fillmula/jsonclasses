from datetime import date, datetime
from ..validators import ChainedValidator, StrValidator, FloatValidator, IntValidator, BoolValidator, DateValidator, DatetimeValidator

def default_validator_for_type(type):
  '''This function returns the default synthesized validator for given Python
  type.

  Args:
    type (Union[str, int, float, bool, date, datetime]): A python type.

  Returns:
    Validator: A synthesized validator for the given Python type or None if it
    can't be synthesized.
  '''
  if type is str:
    return ChainedValidator().append(StrValidator())
  elif type is float:
    return ChainedValidator().append(FloatValidator())
  elif type is int:
    return ChainedValidator().append(IntValidator())
  elif type is bool:
    return ChainedValidator().append(BoolValidator())
  elif type is date:
    return ChainedValidator().append(DateValidator())
  elif type is datetime:
    return ChainedValidator().append(DatetimeValidator())
  else:
    return None
