from __future__ import annotations
from typing import Dict, Any
from ..config import Config
from ..graph import get_registered_class
from ..exceptions import ValidationException
from .validator import Validator
from ..utils import default_validator_for_type, keypath
from dataclasses import fields
from inflection import underscore, camelize
from jsonclasses.utils import *

class InstanceOfValidator(Validator):

  def __init__(self, json_object_class):
    if type(json_object_class) is str:
      self.json_object_class_name = json_object_class
      self.json_object_class = None
    elif hasattr(json_object_class, 'config'):
      self.json_object_class = json_object_class
    else:
      raise ValueError('argument passed to InstanceOfValidator should be subclass of JSONObject.')

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool):
    if value is None:
      return
    if hasattr(self, 'json_object_class_name') and self.json_object_class is None:
      self.json_object_class = get_registered_class(name=self.json_object_class_name, sibling=value.__class__)
    keypath_messages = {}
    for object_field in fields(value):
      default = object_field.default
      if hasattr(default, '__jsonclass_type__'):
        name = object_field.name
        field_value = getattr(value, name)
        try:
          default.validator.validate(field_value, keypath(key_path, name), root, all_fields)
        except ValidationException as exception:
          if all_fields:
            keypath_messages.update(exception.keypath_messages)
          else:
            raise exception
    if len(keypath_messages) > 0:
      raise ValidationException(keypath_messages=keypath_messages, root=root)

  def transform(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config, base: Any = None, fill_blanks: bool = False):
    if value is None:
      return None if not base else base
    if type(value) is not dict:
      return value if not base else base
    if hasattr(self, 'json_object_class_name') and self.json_object_class is None:
      self.json_object_class = get_registered_class(name=self.json_object_class_name, sibling=config.linked_class)
    if not base:
      base = self.json_object_class(__empty=True)
    ### assign values to base
    object_fields = { f.name: f for f in fields(base) }
    unused_names = list(object_fields.keys())
    for raw_key, raw_value in value.items():
      key = underscore(raw_key) if config.camelize_json_keys else raw_key
      if key in unused_names:
        object_field = object_fields[key]
        object_type = object_field.type
        default = object_field.default
        remove_key = True
        if hasattr(default, '__jsonclass_type__'): # user specified types
          # handle readonly (aka no write)
          if is_readonly_type(default.validator):
            remove_key = False
          # handle writeonce (aka write only once)
          elif is_writeonce_type(default.validator):
            current_value = getattr(base, key)
            if current_value is None or hasattr(type(current_value), '__jsonclass_type__'):
              setattr(base, key, default.validator.transform(raw_value, keypath(key_path, key), root, all_fields, config))
            else:
              remove_key = False
          else:
              setattr(base, key, default.validator.transform(raw_value, keypath(key_path, key), root, all_fields, config))
        else:
          validator = default_validator_for_type(object_type)
          if validator is not None: # for supported types, sync a default type for user
            setattr(base, key, validator.transform(raw_value, keypath(key_path, key), root, all_fields, config))
          else:
            setattr(base, key, raw_value)
        if remove_key:
          unused_names.remove(key)
    if fill_blanks:
      for k_with_blank_value in unused_names:
        object_field = object_fields[k_with_blank_value]
        default = object_field.default
        default_factory = object_field.default_factory
        if hasattr(default, '__jsonclass_type__'):
          setattr(base, k_with_blank_value, default.validator.transform(None, keypath(key_path, k_with_blank_value), root, all_fields, config))
        elif default is default_factory:
          setattr(base, k_with_blank_value, None)
        else: # user specified a default value
          setattr(base, k_with_blank_value, default)
    ### end assign
    return base

  def tojson(self, value, config: Config, ignore_writeonly: bool = False):
    if value is None:
      return None
    retval = {}
    object_fields = { f.name: f for f in fields(value) }
    for name, field in object_fields.items():
      key = camelize(name, False) if config.camelize_json_keys else name
      field_value = getattr(value, name)
      default = field.default
      object_type = field.type
      if hasattr(default, '__jsonclass_type__'):
        if is_writeonly_type(default.validator) and not ignore_writeonly:
          continue
        else:
          retval[key] = default.validator.tojson(field_value, config)
      else:
        validator = default_validator_for_type(object_type)
        if validator is not None:
          retval[key] = validator.tojson(field_value, config)
        else:
          retval[key] = field_value
    return retval
