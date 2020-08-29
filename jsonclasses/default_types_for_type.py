from datetime import date, datetime
from .types import types

def default_types_for_type(type):
  if type is str:
    return types.str
  elif type is float:
    return types.float
  elif type is int:
    return types.int
  elif type is bool:
    return types.bool
  elif type is date:
    return types.date
  elif type is datetime:
    return types.datetime
  else:
    return None
