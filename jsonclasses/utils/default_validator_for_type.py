from datetime import date, datetime
from ..validators.chained_validator import ChainedValidator
from ..validators.str_validator import StrValidator
from ..validators.float_validator import FloatValidator
from ..validators.int_validator import IntValidator
from ..validators.bool_validator import BoolValidator
from ..validators.date_validator import DateValidator
from ..validators.datetime_validator import DatetimeValidator

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
