from typing import Optional
from ..types import types, Types
from ..validators import IndexValidator, EagerValidator

def eager_validator_index_after_index(types: Types, index: int) -> Optional[int]:
  '''This function returns the first eager validator index after given index.

  Args:
    types (Types): A jsonclasses types object.

  Returns:
    Optional[int]: The found index or None.
  '''
  vs = types.validator.validators
  try:
    return vs.index(next(v for v in vs[index:] if type(v) is IndexValidator))
  except StopIteration:
    return None
