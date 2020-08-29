from dataclasses import dataclass, fields
from datetime import datetime
from inflection import underscore, camelize
from jsonclasses.types import Types
from jsonclasses.default_types_for_type import default_types_for_type

@dataclass
class JSONObject:

  def __init__(self, **kwargs):
    self._set(fill_blanks=True, **kwargs)

  def to_json(self, camelize_keys=True):
    retval = {}
    object_fields = { f.name: f for f in fields(self) }
    for name, field in object_fields.items():
      key = camelize(name, False) if camelize_keys else name
      value = getattr(self, name)
      default = field.default
      object_type = field.type
      if isinstance(default, Types):
        retval[key] = default.validator.to_json(value)
      else:
        types = default_types_for_type(object_type)
        if types is not None:
          retval[key] = types.validator.to_json(value)
        else:
          retval[key] = value
    return retval

  def _set(self, fill_blanks=True, **kwargs):
    object_fields = { f.name: f for f in fields(self) }
    unused_names = list(object_fields.keys())
    for k, v in kwargs.items():
      underscore_k = underscore(k)
      if underscore_k in unused_names:
        object_field = object_fields[underscore_k]
        object_type = object_field.type
        default = object_field.default
        if isinstance(default, Types):
          setattr(self, underscore_k, default.validator.transform(v))
        else:
          types = default_types_for_type(object_type)
          if types is not None:
            setattr(self, underscore_k, types.validator.transform(v))
          else:
            setattr(self, underscore_k, v)
        unused_names.remove(underscore_k)
    if fill_blanks:
      for k_with_blank_value in unused_names:
        object_field = object_fields[k_with_blank_value]
        default = object_field.default
        default_factory = object_field.default_factory
        if isinstance(default, Types):
          setattr(self, k_with_blank_value, default.validator.transform(None))
        elif default is default_factory:
          setattr(self, k_with_blank_value, None)
        else:
          setattr(self, k_with_blank_value, default)

  def set(self, **kwargs):
    self._set(fill_blanks=False, **kwargs)
    return self
