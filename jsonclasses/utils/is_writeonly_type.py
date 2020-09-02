from datetime import date, datetime
from ..types import types, Types
from ..validators import WriteonlyValidator

def is_writeonly_type(types: Types) -> bool:
  vs = types.validator.validators
  try:
    next(v for v in vs if type(v) is WriteonlyValidator)
    return True
  except StopIteration:
    return False
