from dataclasses import dataclass, fields
from datetime import datetime
from inflection import underscore, camelize

@dataclass
class JsonObject:
  def __init__(self, **kwargs):
    object_fields = fields(self)
    names = []
    types = {}
    for f in object_fields:
      names.append(f.name)
      types[f.name] = f.type
    for k, v in kwargs.items():
      underscore_k = underscore(k)
      if underscore_k in names:
        if types[underscore_k] == datetime:
          setattr(self, underscore_k, datetime.fromisoformat(v))
        else:
          setattr(self, underscore_k, v)
        names.remove(underscore_k)
    for k_with_blank_value in names:
      setattr(self, k_with_blank_value, None)

  def to_json(self):
    retval = {}
    object_fields = fields(self)
    names = []
    types = {}
    for f in object_fields:
      names.append(f.name)
      types[f.name] = f.type
    for k in names:
      value = getattr(self, k)
      if isinstance(value, datetime):
        retval[camelize(k, False)] = value.isoformat()
      else:
        retval[camelize(k, False)] = value
    return retval
