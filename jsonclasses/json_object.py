from __future__ import annotations
from typing import Any, Optional
from dataclasses import dataclass, fields
from datetime import datetime
from functools import reduce
from inflection import underscore, camelize
from jsonclasses.types import Types
from jsonclasses.validators import ChainedValidator, Validator
from jsonclasses.config import Config
from jsonclasses.utils import *
from jsonclasses.exceptions import ValidationException
from .utils.keypath import keypath

@dataclass(init=False)
class JSONObject:
  '''JSONObject is the base class of jsonclass objects. It provides crutial
  instance methods e.g. __init__, set and update, validate and tojson.

  To declare a new jsonclass, use the following syntax:

    from jsonclasses import jsonclass, JSONObject, types

    @jsonclass
    class MyObject(JSONObject):
      my_field_one: str = types.str.required
      my_field_two: int = types.int.range(0, 10).required
  '''

  def __init__(self, **kwargs):
    '''Initialize a new jsonclass object from keyed arguments or a dict. This
    method is suitable for accepting web and malformed inputs. Eager validation
    and transformation are applied during the initialization process.
    '''
    self._set(**kwargs, fill_blanks=True)

  def _set(
    self,
    fill_blanks=False,
    transform=True,
    ignore_eager_validate=False,
    ignore_readonly=False,
    ignore_writeonce=False,
    **kwargs
  ):
    object_fields = { f.name: f for f in fields(self) }
    unused_names = list(object_fields.keys())

    config = Config.on(self.__class__)
    for k, v in kwargs.items():
      key = underscore(k) if config else k
      if key in unused_names:
        object_field = object_fields[key]
        object_type = object_field.type
        default = object_field.default
        remove_key = True
        if isinstance(default, Types): # user specified types
          # handle readonly (aka no write)
          if is_readonly_type(default.validator) and not ignore_readonly:
            remove_key = False
          # handle writeonce (aka write only once)
          elif is_writeonce_type(default.validator) and not ignore_writeonce:
            current_value = getattr(self, key)
            if current_value is None or type(current_value) is Types:
              if transform:
                setattr(self, key, default.validator.transform(v, key, self, False, config))
              else:
                setattr(self, key, v)
            else:
              remove_key = False
          else:
            if transform:
              setattr(self, key, default.validator.transform(v, key, self, False, config))
            else:
              setattr(self, key, v)
        else:
          validator = default_validator_for_type(object_type)
          if validator is not None: # for supported types, sync a default type for user
            if transform:
              setattr(self, key, validator.transform(v, key, self, False, config))
            else:
              setattr(self, key, v)
          else:
            setattr(self, key, v)
        if remove_key:
          unused_names.remove(key)
    if fill_blanks:
      for k_with_blank_value in unused_names:
        object_field = object_fields[k_with_blank_value]
        default = object_field.default
        default_factory = object_field.default_factory
        if isinstance(default, Types):
          if transform:
            setattr(self, k_with_blank_value, default.validator.transform(None, k_with_blank_value, self, False, config))
          else:
            setattr(self, k_with_blank_value, None)
        elif default is default_factory:
          setattr(self, k_with_blank_value, None)
        else: # user specified a default value
          setattr(self, k_with_blank_value, default)

  def set(self, **kwargs):
    '''Set object values in a batch. This method is suitable for web and fraud
    inputs. This method takes accessor marks into consideration, means readonly
    and internal field values will be just ignored. Writeonce fields are
    accepted only if the current value is None. This method triggers eager
    validation and transform. This method returns self, thus you can chain
    calling with other instance methods.
    '''
    self._set(**kwargs)
    return self

  def update(self, **kwargs):
    '''Update object values in a batch. This method is suitable for internal
    inputs. This method ignores accessor marks, thus you can update readonly
    and internal values through this method. Writeonce doesn't have effect on
    this method. You can change writeonce fields' value freely in this method.
    This method does not trigger eager validation and transform. You should
    pass valid and final form values through this method. This method returns
    self, thus you can chain calling with other instance methods.
    '''
    self._set(
      fill_blanks=False,
      transform=False,
      ignore_eager_validate=True,
      ignore_readonly=True,
      ignore_writeonce=True,
      **kwargs
    )
    return self

  def tojson(self, ignore_writeonly=False):
    '''Serialize this jsonclass object to JSON dict.

    Args:
      ignore_writeonly (Optional[bool]): Whether ignore writeonly marks on
      fields. Be careful when setting it to True.

    Returns:
      dict: A dict represents this object's JSON object.
    '''
    config = Config.on(self.__class__)
    camelize_json_keys = config.camelize_json_keys
    retval = {}
    object_fields = { f.name: f for f in fields(self) }
    for name, field in object_fields.items():
      key = camelize(name, False) if camelize_json_keys else name
      value = getattr(self, name)
      default = field.default
      object_type = field.type
      if isinstance(default, Types):
        if is_writeonly_type(default.validator) and not ignore_writeonly:
          continue
        else:
          retval[key] = default.validator.tojson(value, config)
      else:
        validator = default_validator_for_type(object_type)
        if validator is not None:
          retval[key] = validator.tojson(value, config)
        else:
          retval[key] = value
    return retval

  def validate(self, base_key: str = '', root: Any = None, all_fields: bool = True):
    '''Validate the jsonclass object's validity. Raises ValidationException on
    validation failed.

    Args:
      all_fields (bool): Whether continue validation to fetch more error
      messages after the first error is found. This is useful when you are
      building a frontend form and want to display detailed messages.

    Returns:
      None: upon successful validation, returns nothing.
    '''
    if root is None:
      root = self
    keypath_messages = {}
    for object_field in fields(self):
      default = object_field.default
      if isinstance(default, Types):
        name = object_field.name
        value = getattr(self, name)
        try:
          default.validator.validate(value, keypath(base_key, name), root, all_fields)
        except ValidationException as exception:
          if all_fields:
            keypath_messages.update(exception.keypath_messages)
          else:
            raise exception
    if len(keypath_messages) > 0:
      raise ValidationException(keypath_messages=keypath_messages, root=root)
    return self

  def is_valid(self):
    '''Test whether the jsonclass object is valid or not. This method triggers
    object validation.

    Returns:
      bool: the validity of the object.
    '''
    try:
      self.validate(all_fields=False)
    except ValidationException:
      return False
    return True
