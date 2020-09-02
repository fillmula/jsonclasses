from dataclasses import dataclass

def jsonclass(original_class):
  return dataclass(original_class, init=False)

  # unused monkey patch methods
  # klass.__init__ = MethodType(__init__, klass)
  # klass.tojson = MethodType(tojson, klass)
  # return klass
