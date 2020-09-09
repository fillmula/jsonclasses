from __future__ import annotations
from typing import Dict, Any
from ..field_description import FieldDescription, FieldType
from ..config import Config
from ..graph import get_registered_class
from ..exceptions import ValidationException
from .validator import Validator
from dataclasses import fields
from ..fields import fields as our_fields
from inflection import underscore, camelize
from ..utils.is_readonly_type import is_readonly_type
from ..utils.is_writeonly_type import is_writeonly_type
from ..utils.is_writeonce_type import is_writeonce_type
from ..utils.default_validator_for_type import default_validator_for_type
from ..utils.keypath import keypath
from ..utils.reference_map import referenced, resolve_class
from ..fields import collection_argument_type_to_types, fields as our_fields, dataclass_field_to_types
from ..field_description import WriteRule, ReadRule

@referenced
class InstanceOfValidator(Validator):

  def __init__(self, json_object_class):
    if type(json_object_class) is str:
      self.json_object_class_name = json_object_class
      self.json_object_class = None
    elif issubclass(json_object_class, resolve_class('JSONObject')):
      self.json_object_class = json_object_class
    else:
      raise ValueError('argument passed to InstanceOfValidator should be subclass of JSONObject.')

  def define(self, field_description: FieldDescription):
    field_description.field_type = FieldType.INSTANCE

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    if value is None:
      return
    if hasattr(self, 'json_object_class_name') and self.json_object_class is None:
      self.json_object_class = get_registered_class(name=self.json_object_class_name, sibling=config.linked_class)
    keypath_messages = {}
    for our_field in our_fields(value):
      if our_field.field_types:
        field_types = our_field.field_types
        field_name = our_field.field_name
        field_value = getattr(value, field_name)
        try:
          field_types.validator.validate(field_value, keypath(key_path, field_name), root, all_fields, config)
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
    Types = resolve_class('Types')
    if hasattr(self, 'json_object_class_name') and self.json_object_class is None:
      self.json_object_class = get_registered_class(name=self.json_object_class_name, sibling=config.linked_class)
    if not base:
      base = self.json_object_class(__empty=True)
    def fill_blank_with_default_value(field):
      if field.assigned_default_value is not None:
        setattr(base, field.field_name, field.assigned_default_value)
      else:
        transformed_field_value = our_field.field_types.validator.transform(None, keypath(key_path, field.field_name), root, all_fields, config)
        setattr(base, our_field.field_name, transformed_field_value)
    for our_field in our_fields(base):
      if our_field.json_field_name in value.keys() or our_field.field_name in value.keys():
        field_value = value.get(our_field.json_field_name)
        if field_value is None and config.camelize_json_keys:
          field_value = value.get(our_field.field_name)
        if our_field.field_types.field_description.write_rule == WriteRule.NO_WRITE:
          if fill_blanks:
            fill_blank_with_default_value(our_field)
        elif our_field.field_types.field_description.write_rule == WriteRule.WRITE_ONCE:
          current_field_value = getattr(base, our_field.field_name)
          if current_field_value is None or isinstance(current_field_value, Types):
            transformed_field_value = our_field.field_types.validator.transform(field_value, keypath(key_path, our_field.field_name), root, all_fields, config)
            setattr(base, our_field.field_name, transformed_field_value)
          else:
            if fill_blanks:
              fill_blank_with_default_value(our_field)
        else:
          transformed_field_value = our_field.field_types.validator.transform(field_value, keypath(key_path, our_field.field_name), root, all_fields, config)
          setattr(base, our_field.field_name, transformed_field_value)
      else:
        if fill_blanks:
          fill_blank_with_default_value(our_field)
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
      if isinstance(default, resolve_class('Types')):
        if is_writeonly_type(default.validator) and not ignore_writeonly:
          continue
        else:
          retval[key] = default.validator.tojson(field_value, config)
      else:
        validator = default_validator_for_type(object_type, graph_sibling=config.linked_class)
        if validator is not None:
          retval[key] = validator.tojson(field_value, config)
        else:
          retval[key] = field_value
    return retval
