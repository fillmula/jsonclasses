from dataclasses import dataclass, fields
from datetime import datetime
from inflection import underscore, camelize
from jsonclasses.types import Types

@dataclass
class JSONObject:
  def __init__(self, **kwargs):
    object_fields = { f.name: f for f in fields(self) }
    unused_names = list(object_fields.keys())
    for k, v in kwargs.items():
      underscore_k = underscore(k)
      if underscore_k in unused_names:
        types = object_fields[underscore_k].default
        if isinstance(types, Types):
          setattr(self, underscore_k, types.validator.transform(v))
        else:
          setattr(self, underscore_k, v)
        unused_names.remove(underscore_k)
    for k_with_blank_value in unused_names:
      default = object_fields[k_with_blank_value].default
      default_factory = object_fields[k_with_blank_value].default_factory
      if isinstance(default, Types):
        setattr(self, k_with_blank_value, default.validator.transform(None))
      elif default is default_factory:
        setattr(self, k_with_blank_value, None)
      else:
        setattr(self, k_with_blank_value, default)

  def to_json(self):
    retval = {}
    object_fields = { f.name: f for f in fields(self) }
    for name, field in object_fields.items():
      value = getattr(self, name)
      types = field.default
      if isinstance(types, Types):
        retval[camelize(name, False)] = types.validator.to_json(value)
      else:
        retval[camelize(name, False)] = value
    return retval
