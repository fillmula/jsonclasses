from __future__ import annotations
from typing import Any, Optional
from dataclasses import dataclass, fields
from datetime import datetime
from functools import reduce
from inflection import underscore, camelize
from jsonclasses.types import Types
from jsonclasses.validators import ChainedValidator, Validator
from jsonclasses.config import Config
from jsonclasses.exceptions import ValidationException
from .validators.instanceof_validator import InstanceOfValidator
from .utils.reference_map import referenced

@referenced
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

  def __init__(self, __empty: bool = False, **kwargs):
    '''Initialize a new jsonclass object from keyed arguments or a dict. This
    method is suitable for accepting web and malformed inputs. Eager validation
    and transformation are applied during the initialization process.
    '''
    for field in fields(self):
      setattr(self, field.name, None)
    if not __empty:
      self.__set(fill_blanks=True, **kwargs)

  def set(self, **kwargs):
    '''Set object values in a batch. This method is suitable for web and fraud
    inputs. This method takes accessor marks into consideration, means readonly
    and internal field values will be just ignored. Writeonce fields are
    accepted only if the current value is None. This method triggers eager
    validation and transform. This method returns self, thus you can chain
    calling with other instance methods.
    '''
    self.__set(fill_blanks=False, **kwargs)
    return self

  def __set(self, fill_blanks=False, **kwargs):
    validator = InstanceOfValidator(self.__class__)
    config = Config.on(self.__class__)
    validator.transform(kwargs, '', self, True, config, self, fill_blanks)

  def update(self, **kwargs):
    '''Update object values in a batch. This method is suitable for internal
    inputs. This method ignores accessor marks, thus you can update readonly
    and internal values through this method. Writeonce doesn't have effect on
    this method. You can change writeonce fields' value freely in this method.
    This method does not trigger eager validation and transform. You should
    pass valid and final form values through this method. This method returns
    self, thus you can chain calling with other instance methods.
    '''
    unallowed_keys = set(kwargs.keys()) - set(self.__dict__.keys())
    unallowed_keys_length = len(unallowed_keys)
    if unallowed_keys_length:
      keys = 'Keys' if unallowed_keys_length != 1 else 'Key'
      are = 'are' if unallowed_keys_length != 1 else 'is'
      keys_list = ', '.join(list(unallowed_keys))
      raise ValueError(f'{keys} {keys_list} {are} not allowed when updating {self.__class__.__name__}.')
    self.__dict__.update(kwargs)
    return self

  def tojson(self, ignore_writeonly=False):
    '''Serialize this jsonclass object to JSON dict.

    Args:
      ignore_writeonly (Optional[bool]): Whether ignore writeonly marks on
      fields. Be careful when setting it to True.

    Returns:
      dict: A dict represents this object's JSON object.
    '''
    validator = InstanceOfValidator(self.__class__)
    config = Config.on(self.__class__)
    return validator.tojson(self, config, ignore_writeonly=ignore_writeonly)

  def validate(self, all_fields: bool = True):
    '''Validate the jsonclass object's validity. Raises ValidationException on
    validation failed.

    Args:
      all_fields (bool): Whether continue validation to fetch more error
      messages after the first error is found. This is useful when you are
      building a frontend form and want to display detailed messages.

    Returns:
      None: upon successful validation, returns nothing.
    '''
    config = Config.on(self.__class__)
    InstanceOfValidator(self.__class__).validate(self, '', self, all_fields, config)
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
