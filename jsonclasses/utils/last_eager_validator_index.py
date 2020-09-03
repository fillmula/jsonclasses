from typing import Optional, List
from ..validators import Validator, EagerValidator

def last_eager_validator_index(vs: List[Validator]) -> Optional[int]:
  '''This function returns the last eager validator index.

  Args:
    vs (List[Validator]): A list of validators usually from chained validator.

  Returns:
    Optional[int]: The found index or None.
  '''
  try:
    return len(vs) - vs.index(next(v for v in vs[::-1] if type(v) is EagerValidator))
  except StopIteration:
    return None
