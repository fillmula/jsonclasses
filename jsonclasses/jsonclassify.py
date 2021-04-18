"""This module defines the `jsonclassify` function."""
from __future__ import annotations
from typing import Any, Optional, Union
from datetime import datetime
from .jsonclass_object import JSONClassObject
from .contexts import TransformingContext, ValidatingContext, ToJSONContext
from .field_definition import FieldType
from .validators.instanceof_validator import InstanceOfValidator
from .jsonclass_field import JSONClassField
from .isjsonclass import isjsonobject
from .mark_graph import MarkGraph
from .object_graph import ObjectGraph
from .owned_dict import OwnedDict
from .owned_list import OwnedList
from .owned_collection_utils import (to_owned_dict, to_owned_list,
                                     unowned_copy_dict, unowned_copy_list)
from .keypath_utils import concat_keypath, initial_keypath
from .exceptions import (AbstractJSONClassException, ValidationException,
                         JSONClassResetError, JSONClassResetNotEnabledError,
                         UnlinkableJSONClassException)


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
    self._set(kwargs, fill_blanks=True)
    try:
        self._graph.put(self)
    except UnlinkableJSONClassException:
        pass


def jsonobject_set(self: JSONClassObject, **kwargs: dict[str, Any]) -> JSONClassObject:
    """Set object values in a batch. This method is suitable for web and
    fraud inputs. This method takes accessor marks into consideration,
    means readonly and internal field values will be just ignored.
    Writeonce fields are accepted only if the current value is None. This
    method triggers eager validation and transform. This method returns
    self, thus you can chain calling with other instance methods.
    """
    self._ensure_not_detached()
    self._set(kwargs, fill_blanks=False)
    return self


def _set(self: JSONClassObject,
         kwargs: dict[str, Any], fill_blanks: bool = False) -> None:
    """Set values of a jsonclass object internally."""
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
        definition=None,
        all_fields=True,
        dest=self,
        fill_dest_blanks=fill_blanks,
        mark_graph=MarkGraph())
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
                            definition=None,
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
        definition=None,
        all_fields=validate_all_fields,
        mark_graph=MarkGraph())
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
    """This field records values to be reset to. This is only used for fields
    with compare mark or `reset_all_fields` is defined in the class
    configuration.
    """
    return self._previous_values


def reset(self: JSONClassObject) -> None:
    """Reset this object to it's unmodified status.
    """
    if not self.__class__.definition.config.reset_all_fields:
        raise JSONClassResetNotEnabledError()
    if self.is_new:
        raise JSONClassResetError()
    for k, v in self.previous_values.items():
        setattr(self, k, v)
        self._modified_fields = set()
        self._is_modified = False
        self._previous_values = {}


def save(self: JSONClassObject,
         validate_all_fields: bool = False,
         skip_validation: bool = False) -> JSONClassObject:
    """Save this object into database. This will not write if no storage
    modifier is used.
    """
    if not skip_validation:
        self.validate(validate_all_fields=validate_all_fields)
    self._set_on_save()
    self._database_write()
    return self


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
    """Mark the jsonclass object as a new object."""
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
    setattr(self, '_detached_objects', {})
    setattr(self, '_graph', ObjectGraph())


def _mark_not_new(self: JSONClassObject) -> None:
    """Mark the jsonclass object as not a new object."""
    setattr(self, '_is_new', False)


def _add_detached_object(self: JSONClassObject,
                         field_name: str,
                         obj: JSONClassObject) -> None:
    """Add an object into detached objects pool."""
    if not self._detached_objects.get(field_name):
        self._detached_objects[field_name] = []
    if obj not in self._detached_objects[field_name]:
        self._detached_objects[field_name].append(obj)


def _del_detached_object(self: JSONClassObject,
                         field_name: str,
                         obj: JSONClassObject) -> None:
    """Remove an object from detached objects pool."""
    if not self._detached_objects.get(field_name):
        self._detached_objects[field_name] = []
    if obj in self._detached_objects[field_name]:
        self._detached_objects[field_name].remove(obj)


def _clear_detached_object(self: JSONClassObject) -> None:
    """Clear and reset all detached objects."""
    self._detached_objects = {}


def _set_on_save(self: JSONClassObject) -> None:
    """Update fields with setonsave marks if this object is modified. This
    is a graph operation. Objects chained with the saving object will also
    get setonsave called and saved.
    """
    validator = InstanceOfValidator(self.__class__)
    config = self.__class__.definition.config
    context = TransformingContext(
        value=self,
        keypath_root='',
        root=self,
        config_root=config,
        keypath_owner='',
        owner=self,
        config_owner=config,
        keypath_parent='',
        parent=self,
        definition=None,
        mark_graph=MarkGraph())
    validator.serialize(context)


def _clear_temp_fields(self: JSONClassObject) -> None:
    for field in self.__class__.definition.fields:
        if field.definition.is_temp_field:
            setattr(self, field.name, None)


def _database_write(self: JSONClassObject) -> None:
    pass


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
    # track modified and previous value
    if not self.is_new:
        setattr(self, '_is_modified', True)
        self._modified_fields.add(name)
        if self.__class__.definition.config.reset_all_fields or \
                field.definition.has_reset_validator:
            if name not in self.previous_values:
                self.previous_values[name] = getattr(self, name)
    # make list and dict assignments owned and monitored
    if isinstance(value, list):
        value = to_owned_list(self, value, name)
    if isinstance(value, dict):
        value = to_owned_dict(self, value, name)
    if field.definition.is_ref:
        if hasattr(self, name):
            self.__unlink_field__(field, getattr(self, name))
        self.__original_setattr__(name, value)
        self.__link_field__(field, value)
    else:
        self.__original_setattr__(name, value)


def __odict_will_change__(self: JSONClassObject, odict: OwnedDict) -> None:
    # record previous value
    name = initial_keypath(odict.keypath)
    field = self.__class__.definition.field_named(name)
    if self.__class__.definition.config.reset_all_fields or \
            field.definition.has_reset_validator:
        if field.definition.has_linked:
            return
        if name not in self.previous_values:
            if field.definition.field_type == FieldType.DICT:
                self.previous_values[name] = unowned_copy_dict(
                    getattr(self, name))
            if field.definition.field_type == FieldType.LIST:
                self.previous_values[name] = unowned_copy_list(
                    getattr(self, name))


def __odict_add__(self, odict: OwnedDict, key: str, val: Any) -> None:
    if isinstance(val, dict):
        odict[key] = to_owned_dict(self, val,
                                   concat_keypath(odict.keypath, key))
    if isinstance(val, list):
        odict[key] = to_owned_list(self, val,
                                   concat_keypath(odict.keypath, key))
    # record modified
    if not self.is_new:
        setattr(self, '_is_modified', True)
        self._modified_fields.add(odict.keypath)


def __odict_del__(self, odict: OwnedDict, val: Any) -> None:
    # record modified
    if not self.is_new:
        setattr(self, '_is_modified', True)
        self._modified_fields.add(odict.keypath)


def __olist_will_change__(self, olist: OwnedList) -> None:
    # record previous value
    name = initial_keypath(olist.keypath)
    field = self.__class__.definition.field_named(name)
    if self.__class__.definition.config.reset_all_fields or \
            field.definition.has_reset_validator:
        if field.definition.has_linked:
            return
        if name not in self.previous_values:
            if field.definition.field_type == FieldType.DICT:
                self.previous_values[name] = unowned_copy_dict(
                    getattr(self, name))
            if field.definition.field_type == FieldType.LIST:
                self.previous_values[name] = unowned_copy_list(
                    getattr(self, name))


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
    if isinstance(val, dict):
        olist[idx] = to_owned_dict(self, val,
                                   concat_keypath(olist.keypath, idx))
    if isinstance(val, list):
        olist[idx] = to_owned_list(self, val,
                                   concat_keypath(olist.keypath, idx))
    # record modified
    if not self.is_new:
        setattr(self, '_is_modified', True)
        self._modified_fields.add(olist.keypath)


def __olist_del__(self: JSONClassObject, olist: OwnedList, val: Any) -> None:
    class_definition = self.__class__.definition
    try:
        field = class_definition.field_named(olist.keypath)
    except ValueError:
        field = None
    if field and field.definition.is_ref:
        self.__unlink_field__(field, [val])
    # record modified
    if not self.is_new:
        setattr(self, '_is_modified', True)
        self._modified_fields.add(olist.keypath)


def __olist_sor__(self, olist: OwnedList) -> None:
    # record modified
    if not self.is_new:
        setattr(self, '_is_modified', True)
        self._modified_fields.add(olist.keypath)


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
        self._add_detached_object(field.name, item)
        other_field = field.foreign_field
        if other_field is None:
            return
        if other_field.definition.field_type == FieldType.INSTANCE:
            if getattr(item, other_field.name) is self:
                item.__original_setattr__(other_field.name, None)
                item._add_detached_object(other_field.name, self)
        elif other_field.definition.field_type == FieldType.LIST:
            other_list = getattr(item, other_field.name)
            if isinstance(other_list, list):
                if self in other_list:
                    other_list.remove(self)
                    item._add_detached_object(other_field.name, self)


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
        self._del_detached_object(field.name, item)
        other_field = field.foreign_field
        if other_field is None:
            return
        if other_field.definition.field_type == FieldType.INSTANCE:
            if getattr(item, other_field.name) != self:
                setattr(item, other_field.name, self)
                item._del_detached_object(other_field.name, self)
        elif other_field.definition.field_type == FieldType.LIST:
            if not isinstance(getattr(item, other_field.name), list):
                setattr(item, other_field.name, [self])
                item._del_detached_object(other_field.name, self)
            else:
                if self not in getattr(item, other_field.name):
                    getattr(item, other_field.name).append(self)
                    item._del_detached_object(other_field.name, self)
        self.__link_graph__(item)


def __link_graph__(self: JSONClassObject, other: JSONClassObject) -> None:
    """
    """
    try:
        if not self._graph.has(self):
            self._graph.put(self)
    except UnlinkableJSONClassException:
        pass
    self._graph.merged_graph(other._graph)


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
    class_.set = jsonobject_set
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
    class_.previous_values = previous_values
    class_.reset = reset
    class_.save = save
    # protected methods
    class_._ensure_not_detached = _ensure_not_detached
    class_._data_dict = _data_dict
    class_._mark_new = _mark_new
    class_._set_initial_status = _set_initial_status
    class_._mark_not_new = _mark_not_new
    class_._add_detached_object = _add_detached_object
    class_._del_detached_object = _del_detached_object
    class_._clear_detached_object = _clear_detached_object
    class_._set_on_save = _set_on_save
    class_._clear_temp_fields = _clear_temp_fields
    class_._database_write = _database_write
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
    class_.__link_graph__ = __link_graph__
    return class_
