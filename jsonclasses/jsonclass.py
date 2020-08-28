from dataclasses import dataclass
# from datetime import datetime
# from inflection import underscore, camelize
# from types import MethodType

def jsonclass(original_class):
  return dataclass(original_class, init=False)
  # def __init__(self, **kwargs):
  #   object_fields = fields(self)
  #   names = []
  #   types = {}
  #   for f in object_fields:
  #     names.append(f.name)
  #     types[f.name] = f.type
  #   for k, v in kwargs.items():
  #     underscore_k = underscore(k)
  #     if underscore_k in names:
  #       if types[underscore_k] == datetime:
  #         setattr(self, underscore_k, datetime.fromisoformat(v))
  #       else:
  #         setattr(self, underscore_k, v)
  #       names.remove(underscore_k)
  #   for k_with_blank_value in names:
  #     setattr(self, k_with_blank_value, None)
  # def to_json(self):
  #   retval = {}
  #   object_fields = fields(self)
  #   names = []
  #   types = {}
  #   for f in object_fields:
  #     names.append(f.name)
  #     types[f.name] = f.type
  #   for k in names:
  #     value = getattr(self, k)
  #     if isinstance(value, datetime):
  #       retval[camelize(k, False)] = value.isoformat()
  #     else:
  #       retval[camelize(k, False)] = value
  #   return retval
  # klass.__init__ = MethodType(__init__, klass)
  # klass.to_json = MethodType(to_json, klass)
  # return klass
