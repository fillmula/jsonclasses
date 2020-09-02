from dataclasses import dataclass, fields
from datetime import datetime
from inflection import underscore, camelize
from jsonclasses.types import Types
from jsonclasses.utils import *
from jsonclasses.exceptions import ValidationException

@dataclass
class JSONObject:

  def __init__(self, **kwargs):
    self._set(**kwargs, fill_blanks=True)

  def _set(
    self,
    fill_blanks=False,
    transform=True,
    validate=True,
    ignore_readonly=False,
    ignore_writeonce=False,
    **kwargs
  ):
    object_fields = { f.name: f for f in fields(self) }
    unused_names = list(object_fields.keys())
    for k, v in kwargs.items():
      underscore_k = underscore(k)
      if underscore_k in unused_names:
        object_field = object_fields[underscore_k]
        object_type = object_field.type
        default = object_field.default
        remove_key = True
        if isinstance(default, Types): # user specified types
          # handle readonly (aka no write)
          if is_readonly_type(default) and not ignore_readonly:
            remove_key = False
          # handle writeonce (aka write only once)
          elif is_writeonce_type(default) and not ignore_writeonce:
            current_value = getattr(self, underscore_k)
            if current_value is None or type(current_value) is Types:
              if transform:
                setattr(self, underscore_k, default.validator.transform(v))
              else:
                setattr(self, underscore_k, v)
            else:
              remove_key = False
          else:
            if transform:
              setattr(self, underscore_k, default.validator.transform(v))
            else:
              setattr(self, underscore_k, v)
        else:
          types = default_types_for_type(object_type)
          if types is not None: # for supported types, sync a default type for user
            if transform:
              setattr(self, underscore_k, types.validator.transform(v))
            else:
              setattr(self, underscore_k, v)
          else:
            setattr(self, underscore_k, v)
        if remove_key:
          unused_names.remove(underscore_k)
    if fill_blanks:
      for k_with_blank_value in unused_names:
        object_field = object_fields[k_with_blank_value]
        default = object_field.default
        default_factory = object_field.default_factory
        if isinstance(default, Types):
          if transform:
            setattr(self, k_with_blank_value, default.validator.transform(None))
          else:
            setattr(self, k_with_blank_value, None)
        elif default is default_factory:
          setattr(self, k_with_blank_value, None)
        else: # user specified a default value
          setattr(self, k_with_blank_value, default)

  def set(self, **kwargs):
    self._set(**kwargs)
    return self

  def update(self, **kwargs):
    self._set(
      fill_blanks=False,
      validate=False,
      transform=False,
      ignore_readonly=True,
      ignore_writeonce=True,
      **kwargs
    )
    return self

  def tojson(self, camelize_keys=True, ignore_writeonly=False):
    retval = {}
    object_fields = { f.name: f for f in fields(self) }
    for name, field in object_fields.items():
      key = camelize(name, False) if camelize_keys else name
      value = getattr(self, name)
      default = field.default
      object_type = field.type
      if isinstance(default, Types):
        if is_writeonly_type(default) and not ignore_writeonly:
          continue
        else:
          retval[key] = default.validator.tojson(value)
      else:
        types = default_types_for_type(object_type)
        if types is not None:
          retval[key] = types.validator.tojson(value)
        else:
          retval[key] = value
    return retval

  def validate(self, all_fields=True):
    keypath_messages = {}
    for object_field in fields(self):
      default = object_field.default
      if isinstance(default, Types):
        name = object_field.name
        value = getattr(self, name)
        try:
          default.validator.validate(value, name, self, all_fields)
        except ValidationException as exception:
          if all_fields:
            keypath_messages.update(exception.keypath_messages)
          else:
            raise exception
    if len(keypath_messages) > 0:
      raise ValidationException(keypath_messages=keypath_messages, root=self)
    return self

  def is_valid(self):
    try:
      self.validate(all_fields=False)
    except ValidationException:
      return False
    return True
