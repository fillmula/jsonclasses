from typing import Any, get_origin, get_args
from datetime import date, datetime
from .reference_map import resolve_class
from ..graph import get_registered_class, JSONClassNotFoundError

def default_validator_for_type(type: Any, graph_sibling: Any = None):
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
  elif get_origin(type) is not None:
    origin = get_origin(type)
    if origin is list:
      inner_validator = default_validator_for_type(get_args(type)[0])
      ListOfValidator = resolve_class('ListOfValidator')
      return ChainedValidator().append(ListOfValidator(inner_validator))
    elif origin is dict:
      inner_validator = default_validator_for_type(get_args(type)[1])
      DictOfValidator = resolve_class('DictOfValidator')
      return ChainedValidator().append(DictOfValidator(inner_validator))
    else:
      return None
  elif isinstance(type, str):
    if type == 'str':
      return default_validator_for_type(str)
    elif type == 'int':
      return default_validator_for_type(int)
    elif type == 'float':
      return default_validator_for_type(float)
    elif type == 'bool':
      return default_validator_for_type(bool)
    elif type == 'date':
      return default_validator_for_type(date)
    elif type == 'datetime':
      return default_validator_for_type(datetime)
    else:
      InstanceOfValidator = resolve_class('InstanceOfValidator')
      cls = get_registered_class(type, sibling=graph_sibling)
      return ChainedValidator().append(InstanceOfValidator(cls))
  elif issubclass(type, resolve_class('JSONObject')):
    InstanceOfValidator = resolve_class('InstanceOfValidator')
    return ChainedValidator().append(InstanceOfValidator(type))
  else:
    return None
