from dataclasses import dataclass

def jsonclass(original_class):
  return dataclass(original_class, init=False)

  # unused monkey patch methods

  # klass.__init__ = MethodType(__init__, klass)
  # klass.to_json = MethodType(to_json, klass)
  # return klass
