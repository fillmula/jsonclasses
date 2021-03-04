"""This module defines the `jsonclassify` function."""
from __future__ import annotations
from jsonclasses.field_definition import FieldType
from typing import Any, Optional, Union
from datetime import datetime
from .jsonclass_object import JSONClassObject
from .contexts import TransformingContext, ValidatingContext, ToJSONContext
from .validators.instanceof_validator import InstanceOfValidator
from .jsonclass_field import JSONClassField
from .isjsonclass import isjsonobject, isjsonclass
from .object_graph import ObjectGraph
from .owned_dict import OwnedDict
from .owned_list import OwnedList
from .owned_collection_utils import to_owned_dict, to_owned_list
from .keypath_utils import concat_keypath
from .exceptions import AbstractJSONClassException, ValidationException


def __init__(self: JSONClassObject, **kwargs: dict[str, Any]) -> None:
    """Initialize a new jsonclass object from keyed arguments or a dict.
    This method is suitable for accepting web and malformed inputs. Eager
    validation and transformation are applied during the initialization
    process.
    """
    if self.__class__.definition.config.abstract:
        raise AbstractJSONClassException(self.__class__)
    self._set_initial_status()
    for field in self.__class__.definition.fields:
        setattr(self, field.name, None)
    self._set(fill_blanks=True, **kwargs)


def j_set(self: JSONClassObject, **kwargs: dict[str, Any]) -> JSONClassObject:
    """Set object values in a batch. This method is suitable for web and
    fraud inputs. This method takes accessor marks into consideration,
    means readonly and internal field values will be just ignored.
    Writeonce fields are accepted only if the current value is None. This
    method triggers eager validation and transform. This method returns
    self, thus you can chain calling with other instance methods.
    """
    self._ensure_not_detached()
    self._set(fill_blanks=False, **kwargs)
    return self


def _set(self: JSONClassObject, fill_blanks: bool = False, **kwargs: dict[str, Any]) -> None:
    """Set values of a JSON Class object internally."""
    validator = InstanceOfValidator(self.__class__)
    config = self.__class__.definition.config
    context = TransformingContext(
        value=kwargs,
        keypath_root='',
        root=self,
        config_root=config,
        keypath_owner='',
        owner=self,
        config_owner=config,
        keypath_parent='',
        parent=self,
        fdesc=None,
        all_fields=True,
        dest=self,
        fill_dest_blanks=fill_blanks,
        object_graph=self._graph)
    validator.transform(context)


def update(self: JSONClassObject, **kwargs: dict[str, Any]) -> JSONClassObject:
    """Update object values in a batch. This method is suitable for
    internal inputs. This method ignores accessor marks, thus you can
    update readonly and internal values through this method. Writeonce
    doesn't have effect on this method. You can change writeonce fields'
    value freely in this method. This method does not trigger eager
    validation and transform. You should pass valid and final form values
    through this method. This method returns self, thus you can chain
    calling with other instance methods.
    """
    self._ensure_not_detached()
    unallowed_keys = set(kwargs.keys()) - set(self._data_dict.keys())
    unallowed_keys_length = len(unallowed_keys)
    if unallowed_keys_length > 0:
        keys_list = "', '".join(list(unallowed_keys))
        raise ValueError(f"'{keys_list}' not allowed in "
                         f"{self.__class__.__name__}.")
    for key, item in kwargs.items():
        setattr(self, key, item)
    return self


def tojson(self: JSONClassObject,
           ignore_writeonly: bool = False) -> dict[str, Any]:
    """Convert this JSON Class object to JSON dict.

    Args:
        ignore_writeonly (Optional[bool]): Whether ignore writeonly marks on
        fields. Be careful when setting it to True.

    Returns:
        dict[str, Any]: A dict represents this object's JSON object.
    """
    self._ensure_not_detached()
    validator = InstanceOfValidator(self.__class__)
    config = self.__class__.definition.config
    context = ToJSONContext(value=self,
                            config=config,
                            ignore_writeonly=ignore_writeonly)
    return validator.tojson(context)


def validate(self: JSONClassObject,
             validate_all_fields: Optional[bool] = None) -> JSONClassObject:
    """Validate the jsonclass object's validity. Raises ValidationException
    on validation failed.

    Args:
        validate_all_fields (bool): Whether continue validation to fetch more
        error messages after the first error is found. This is useful when you
        are building a frontend form and want to display detailed messages.

    Returns:
        None: upon successful validation, returns nothing.
    """
    self._ensure_not_detached()
    config = self.__class__.definition.config
    context = ValidatingContext(
        value=self,
        keypath_root='',
        root=self,
        config_root=config,
        keypath_owner='',
        owner=self,
        config_owner=config,
        keypath_parent='',
        parent=self,
        fdesc=None,
        all_fields=validate_all_fields,
        object_graph=ObjectGraph())
    InstanceOfValidator(self.__class__).validate(context)
    return self


@property
def is_valid(self: JSONClassObject) -> bool:
    """Test whether the jsonclass object is valid or not. This method
    triggers object validation.

    Returns:
        bool: the validity of the object.
    """
    try:
        self.validate(validate_all_fields=False)
    except ValidationException:
        return False
    return True


@property
def is_new(self: JSONClassObject) -> bool:
    """This property is true if this object is newly created and not persisted
    yet.
    """
    return self._is_new


@property
def is_modified(self: JSONClassObject) -> bool:
    """This property indicates this object is modified and it's a new version
    comparing to the persisted one in the database. Calling save will cause
    modified fields to be written into the persistance storage.
    """
    return self._is_modified


@property
def is_detached(self: JSONClassObject) -> bool:
    """If a JSON class object is detached. This object cannot be used anymore
    since it represents an outdated state of the same database record.
    """
    return self._is_detached


@property
def is_deleted(self: JSONClassObject) -> bool:
    """This property records whether this object is deleted."""
    return self._is_deleted


@property
def modified_fields(self: JSONClassObject) -> tuple[str]:
    """A tuple of string represents the modified field names which need
    validation.
    """
    return tuple(self._modified_fields)


@property
def persisted_modified_fields(self: JSONClassObject) -> tuple[str]:
    """This is similar to `modified_fields`. This property doesn't include
    temporary fields. Thus, use `persisted_modified_fields` when updating the
    database.
    """
    retval: list[str] = []
    class_definition = self.__class__.definition
    for name in self._modified_fields:
        if not class_definition.field_named(name).definition.is_temp_field:
            retval.append(name)
    return tuple(retval)


@property
def previous_values(self: JSONClassObject) -> dict[str, Any]:
    """
    """
    return self._previous_values


def _ensure_not_detached(self: JSONClassObject) -> None:
    """Raises if this JSON class object is detached.

    Raises:
        ValueError: This exception is raised if the object is detached.
    """
    if self.is_detached:
        raise ValueError(f'JSON class object {self} is detached')


@property
def _data_dict(self: JSONClassObject) -> dict[str, Any]:
    """A dict which is a subview of __dict__ that only contains public data
    field items.
    """
    retval = {}
    for k, v in self.__dict__.items():
        if not k.startswith('_'):
            retval[k] = v
    return retval


def _mark_new(self: JSONClassObject) -> None:
    """Mark the JSON class object as a new object."""
    setattr(self, '_is_new', True)
    setattr(self, '_is_modified', False)
    setattr(self, '_modified_fields', set())
    setattr(self, '_previous_values', {})


def _set_initial_status(self: JSONClassObject) -> None:
    """Set the initial status of the JSON class object."""
    self._mark_new()
    setattr(self, '_is_detached', False)
    setattr(self, '_is_deleted', False)
    setattr(self, '_previous_values', {})
    setattr(self, '_graph', ObjectGraph())


@property
def _id(self: JSONClassObject) -> Union[str, int, None]:
    field = self.__class__.definition.primary_field
    if not field:
        return None
    return getattr(self, field.name)


@property
def _created_at(self: JSONClassObject) -> datetime:
    field = self.__class__.definition.created_at_field
    if not field:
        return None
    return getattr(self, field.name)


@property
def _updated_at(self: JSONClassObject) -> datetime:
    field = self.__class__.definition.updated_at_field
    if not field:
        return None
    return getattr(self, field.name)


@property
def _deleted_at(self: JSONClassObject) -> datetime:
    field = self.__class__.definition.deleted_at_field
    if not field:
        return None
    return getattr(self, field.name)


def __is_private_attr__(name: str) -> bool:
    """Returns true if the attribute name indicates private attribute."""
    return name.startswith('_')


def __setattr__(self: JSONClassObject, name: str, value: Any) -> None:
    # use original setattr for private fields
    if __is_private_attr__(name):
        self.__original_setattr__(name, value)
        return
    # use original setattr for non JSON class fields
    try:
        field = self.__class__.definition.field_named(name)
    except ValueError:
        self.__original_setattr__(name, value)
        return
    # this is a JSON class field attribute
    self._ensure_not_detached()
    if hasattr(self, name) and value == getattr(self, name):
        return
    # make list and dict assignments owned and monitored
    if isinstance(value, list):
        value = to_owned_list(self, value, name)
    if isinstance(value, dict):
        value = to_owned_dict(self, value, name)
    if field.definition.is_ref:
        self.__unlink_field__(field, getattr(self, name))
        self.__original_setattr__(name, value)
        self.__link_field__(field, value)
    else:
        self.__original_setattr__(name, value)


def __odict_will_change__(self, odict: OwnedDict) -> None:
    pass


def __odict_add__(self, odict: OwnedDict, key: str, val: Any) -> None:
    if isinstance(val, dict):
        odict[key] = to_owned_dict(self, val,
                                   concat_keypath(odict.keypath, key))
    if isinstance(val, list):
        odict[key] = to_owned_list(self, val,
                                   concat_keypath(odict.keypath, key))


def __odict_del__(self, odict: OwnedDict, val: Any) -> None:
    pass


def __olist_will_change__(self, olist: OwnedList) -> None:
    pass


def __olist_add__(self: JSONClassObject,
                  olist: OwnedList,
                  idx: int,
                  val: Any) -> None:
    class_definition = self.__class__.definition
    try:
        field = class_definition.field_named(olist.keypath)
    except ValueError:
        field = None
    if field is not None and field.definition.is_ref:
        self.__link_field__(field, [val])
        return
    if isinstance(val, dict):
        olist[idx] = to_owned_dict(self, val,
                                   concat_keypath(olist.keypath, idx))
    if isinstance(val, list):
        olist[idx] = to_owned_list(self, val,
                                   concat_keypath(olist.keypath, idx))


def __olist_del__(self: JSONClassObject, olist: OwnedList, val: Any) -> None:
    class_definition = self.__class__.definition
    try:
        field = class_definition.field_named(olist.keypath)
    except ValueError:
        field = None
    if field is None:
        return
    if not field.definition.is_ref:
        return
    self.__unlink_field__(field, [val])


def __olist_sor__(self, olist: OwnedList) -> None:
    pass


def __unlink_field__(self: JSONClassObject,
                     field: JSONClassField,
                     value: Any) -> None:
    items: list[JSONClassObject] = []
    if field.definition.field_type == FieldType.INSTANCE:
        if not isjsonobject(value):
            return
        items = [value]
    if field.definition.field_type == FieldType.LIST:
        if not isinstance(value, list):
            return
        items = list(value)
    for item in items:
        other_field = field.foreign_field
        if other_field is None:
            return
        if other_field.definition.field_type == FieldType.INSTANCE:
            if getattr(item, other_field.name) is self:
                item.__original_setattr__(other_field.name, None)
        elif other_field.definition.field_type == FieldType.LIST:
            other_list = getattr(item, other_field.name)
            if isinstance(other_list, list):
                if self in other_list:
                    other_list.remove(self)


def __link_field__(self: JSONClassObject,
                   field: JSONClassField,
                   value: Any) -> None:
    items: list[JSONClassObject] = []
    if field.definition.field_type == FieldType.INSTANCE:
        if not isjsonobject(value):
            return
        items = [value]
    if field.definition.field_type == FieldType.LIST:
        if not isinstance(value, list):
            return
        items = value
    for item in items:
        other_field = field.foreign_field
        if other_field is None:
            return
        if other_field.definition.field_type == FieldType.INSTANCE:
            if getattr(item, other_field.name) != self:
                setattr(item, other_field.name, self)
        elif other_field.definition.field_type == FieldType.LIST:
            if not isinstance(getattr(item, other_field.name), list):
                setattr(item, other_field.name, [self])
            else:
                if self not in getattr(item, other_field.name):
                    getattr(item, other_field.name).append(self)
    self.__link_graph__(item)


def jsonclassify(class_: type) -> JSONClassObject:
    """Make a declared class into JSON class.

    Args:
        class_ (type): A class that user declared.

    Returns:
        JSONClassObject: A class that confirms to `JSONClassObject`.
    """
    # do not install methods for subclasses
    if hasattr(class_, '__is_jsonclass__'):
        return class_
    # type marks
    class_.__is_jsonclass__ = True
    # public methods
    class_.__init__ = __init__
    class_.set = j_set
    class_._set = _set
    class_.update = update
    class_.tojson = tojson
    class_.validate = validate
    class_.is_valid = is_valid
    class_.is_new = is_new
    class_.is_modified = is_modified
    class_.is_detached = is_detached
    class_.is_deleted = is_deleted
    class_.modified_fields = modified_fields
    class_.persisted_modified_fields = persisted_modified_fields
    # protected methods
    class_._ensure_not_detached = _ensure_not_detached
    class_._data_dict = _data_dict
    class_._mark_new = _mark_new
    class_._set_initial_status = _set_initial_status
    class_._id = _id
    class_._created_at = _created_at
    class_._updated_at = _updated_at
    class_._deleted_at = _deleted_at
    # private methods
    class_.__original_setattr__ = class_.__setattr__
    class_.__setattr__ = __setattr__
    class_.__odict_will_change__ = __odict_will_change__
    class_.__odict_add__ = __odict_add__
    class_.__odict_del__ = __odict_del__
    class_.__olist_will_change__ = __olist_will_change__
    class_.__olist_add__ = __olist_add__
    class_.__olist_del__ = __olist_del__
    class_.__olist_sor__ = __olist_sor__
    class_.__unlink_field__ = __unlink_field__
    class_.__link_field__ = __link_field__
    return class_
