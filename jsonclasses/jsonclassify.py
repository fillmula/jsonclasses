"""This module defines the `jsonclassify` function."""
from __future__ import annotations
from typing import Any, Callable, Optional, Union
from inspect import signature, getmro
from .jobject import JObject
from .ctx import Ctx, CtxCfg
from .fdef import Fdef, FStore, FType
from .types import Types
from .modifiers.instanceof_modifier import InstanceOfModifier
from .jfield import JField
from .isjsonclass import isjsonobject
from .mgraph import MGraph
from .ograph import OGraph
from .odict import OwnedDict
from .olist import OwnedList
from .outils import (
    to_owned_dict, to_owned_list, unowned_copy_dict, unowned_copy_list
)
from .keypath import (
    concat_keypath, initial_keypath, single_key_args, compound_key_args,
    keypath_split
)
from .excs import (AbstractJSONClassException, ValidationException,
                         JSONClassResetError, JSONClassResetNotEnabledError,
                         UnlinkableJSONClassException,
                         UnauthorizedActionException)



def __init__(self: JObject, **kwargs: dict[str, Any]) -> None:
    """Initialize a new jsonclass object from keyed arguments or a dict.
    This method is suitable for accepting web and malformed inputs. Eager
    validation and transformation are applied during the initialization
    process.
    """
    if self.__class__.cdef.jconf.abstract:
        raise AbstractJSONClassException(self.__class__)
    self._set_initial_status()
    for field in self.__class__.cdef.fields:
        if field.fdef.fstore != FStore.CALCULATED:
            setattr(self, field.name, None)
        if field.fdef.fstore == FStore.LOCAL_KEY:
            transformer = self.__class__.cdef.jconf.ref_key_encoding_strategy
            local_key = transformer(field)
            if field.fdef.ftype == FType.LIST:
                setattr(self, local_key, to_owned_list(self, [], local_key))
            else:
                setattr(self, local_key, None)
            self._local_keys.add(local_key)
            self._local_key_map[local_key] = field.name
    self._set(single_key_args(kwargs), fill_blanks=True)
    self._keypath_set(compound_key_args(kwargs))
    try:
        self._graph.put(self)
    except UnlinkableJSONClassException:
        pass


def jsonobject_set(self: JObject, **kwargs: dict[str, Any]) -> JObject:
    """Set object values in a batch. This method is suitable for web and
    fraud inputs. This method takes accessor marks into consideration,
    means readonly and internal field values will be just ignored.
    Writeonce fields are accepted only if the current value is None. This
    method triggers eager validation and transform. This method returns
    self, thus you can chain calling with other instance methods.
    """
    self._set(single_key_args(kwargs), fill_blanks=False)
    self._keypath_set(compound_key_args(kwargs))
    return self


def _set(self: JObject,
         kwargs: dict[str, Any], fill_blanks: bool = False) -> None:
    """Set values of a jsonclass object internally."""
    ctxcfg = CtxCfg(fill_dest_blanks=fill_blanks, all_fields=False)
    ctx = Ctx.rootctx(self, ctxcfg, kwargs)
    InstanceOfModifier(self.__class__).transform(ctx)


def _keypath_set(self: JObject, kwargs: dict[str, Any]) -> None:
    for key, value in kwargs.items():
        items = keypath_split(key)
        dest = getattr(self, items[0])
        fdef = self.__class__.cdef.field_named(items[0]).types.fdef
        used_items = [items[0]]
        self._set_to_container(dest, items[1:], value, fdef, used_items)


def _set_to_container(self: JObject,
                      dest: Any,
                      items: list[str],
                      value: Any,
                      fdef: Fdef,
                      used_items: list[str]) -> None:
    if fdef.ftype == FType.INSTANCE:
        if dest is None:
            raise ValueError(f"value in {'.'.join(used_items)} is None")
        if len(items) == 1:
            dest._set({items[0]: value}, fill_blanks=False)
        else:
            dest._keypath_set({'.'.join(items): value})
    elif fdef.ftype == FType.LIST:
        if dest is None:
            raise ValueError(f"value in {'.'.join(used_items)} is None")
        if len(items) == 1:
            dest[int(items[0])] = value
        else:
            fdef = fdef.item_types.fdef
            self._set_to_container(dest[int(items[0])], items[1:], value, fdef, used_items + [items[0]])
    elif fdef.ftype == FType.DICT:
        if dest is None:
            raise ValueError(f"value in {'.'.join(used_items)} is None")
        if len(items) == 1:
            dest[items[0]] = value
        else:
            fdef = fdef.item_types.fdef
            self._set_to_container(dest[items[0]], items[1:], value, fdef, used_items + [items[0]])


def update(self: JObject, **kwargs: dict[str, Any]) -> JObject:
    """Update object values in a batch. This method is suitable for
    internal inputs. This method ignores accessor marks, thus you can
    update readonly and internal values through this method. Writeonce
    doesn't have effect on this method. You can change writeonce fields'
    value freely in this method. This method does not trigger eager
    validation and transform. You should pass valid and final form values
    through this method. This method returns self, thus you can chain
    calling with other instance methods.
    """
    unallowed_keys = (set(kwargs.keys())
                      - set(self.__class__.cdef.update_names))
    unallowed_keys_length = len(unallowed_keys)
    if unallowed_keys_length > 0:
        keys_list = "', '".join(list(unallowed_keys))
        raise ValueError(f"'{keys_list}' not allowed in "
                         f"{self.__class__.__name__}.")
    for key, item in kwargs.items():
        setattr(self, key, item)
    return self


def tojson(self: JObject,
           ignore_writeonly: bool = False,
           reverse_relationship: bool = False) -> dict[str, Any]:
    """Convert this JSON Class object to JSON dict.

    Args:
        ignore_writeonly (bool): Whether ignore writeonly marks on
        fields. Be careful when setting it to True.

        reverse_relationship (bool): Whether including reverse relationship in
        json outputs.

    Returns:
        dict[str, Any]: A dict represents this object's JSON object.
    """
    self._can_read_check()
    ctxcfg = CtxCfg(ignore_writeonly=ignore_writeonly,
                    reverse_relationship=reverse_relationship)
    ctx = Ctx.rootctx(self, ctxcfg)
    return InstanceOfModifier(self.__class__).tojson(ctx)


def validate(self: JObject, all_fields: Optional[bool] = None) -> JObject:
    """Validate the jsonclass object's validity. Raises ValidationException
    on validation failed.

    Args:
        validate_all_fields (bool): Whether continue validation to fetch more
        error messages after the first error is found. This is useful when you
        are building a frontend form and want to display detailed messages.

    Returns:
        None: upon successful validation, returns nothing.
    """
    ctxcfg = CtxCfg(all_fields=all_fields)
    ctx = Ctx.rootctx(self, ctxcfg)
    InstanceOfModifier(self.__class__).validate(ctx)
    return self


@property
def is_valid(self: JObject) -> bool:
    """Test whether the jsonclass object is valid or not. This method
    triggers object validation.

    Returns:
        bool: the validity of the object.
    """
    try:
        self.validate(all_fields=False)
    except ValidationException:
        return False
    return True


def opby(self: JObject, operator: Any) -> JObject:
    """Assigns an operator object to the current object. This is used for
    operator based validation.

    Args:
        operator (Any): Anything that is operator defined by user.

    Returns:
        JObject: The JObject itself is returned.
    """
    setattr(self, '_operator', operator)
    if self.is_new:
        class_def = self.__class__.cdef
        for field in class_def.assign_operator_fields:
            if field.fdef.operator_assign_transformer is not None:
                transformer = field.fdef.operator_assign_transformer
                params_len = len(signature(transformer).parameters)
                if params_len == 1:
                    setattr(self, field.name, transformer(operator))
                elif params_len == 2:
                    setattr(self, field.name, transformer(operator, self))
            else:
                setattr(self, field.name, operator)
    return self


@property
def is_new(self: JObject) -> bool:
    """This property is true if this object is newly created and not persisted
    yet.
    """
    return self._is_new


@property
def is_modified(self: JObject) -> bool:
    """This property indicates this object is modified and it's a new version
    comparing to the persisted one in the database. Calling save will cause
    modified fields to be written into the persistance storage.
    """
    return self._is_modified


@property
def is_partial(self: JObject) -> bool:
    """This property indicates this object is not a full version of the item it
    represents in the database. Only part of fields are fetched from the
    database.
    """
    return self._is_partial


@property
def is_deleted(self: JObject) -> bool:
    """This property records whether this object is deleted."""
    return self._is_deleted


@property
def modified_fields(self: JObject) -> tuple[str]:
    """A tuple of string represents the modified field names which need
    validation.
    """
    return tuple(self._modified_fields)


@property
def persisted_modified_fields(self: JObject) -> tuple[str]:
    """This is similar to `modified_fields`. This property doesn't include
    temporary fields. Thus, use `persisted_modified_fields` when updating the
    database.
    """
    retval: list[str] = []
    cdef = self.__class__.cdef
    for name in self._modified_fields:
        if cdef.field_named(name).fdef.fstore != FStore.TEMP:
            retval.append(name)
    return tuple(retval)


@property
def previous_values(self: JObject) -> dict[str, Any]:
    """This field records values to be reset to. This is only used for fields
    with compare mark or `reset_all_fields` is defined in the class
    configuration.
    """
    return self._previous_values


@property
def unlinked_objects(self: JObject) -> dict[str, list[JObject]]:
    """Unlinked objects of this jsonclass object.
    """
    return self._unlinked_objects


def reset(self: JObject) -> None:
    """Reset this object to it's unmodified status.
    """
    if not self.__class__.cdef.jconf.reset_all_fields:
        raise JSONClassResetNotEnabledError()
    if self.is_new:
        raise JSONClassResetError()
    for k, v in self.previous_values.items():
        setattr(self, k, v)
        self._modified_fields = set()
        self._is_modified = False
        self._previous_values = {}


def save(self: JObject,
         validate_all_fields: bool = False,
         skip_validation: bool = False) -> JObject:
    """Save this object into database. This will not write if no storage
    modifier is used.
    """
    self._can_create_or_update_check()
    if self.is_new:
        self._run_on_create_callbacks()
    else:
        self._run_on_update_callbacks()
    if not skip_validation:
        self.validate(all_fields=validate_all_fields)
    self._set_on_save()
    self._database_write()
    for _, lst in self.unlinked_objects.items():
        for item in lst:
            lst.remove(item)
            item.save(validate_all_fields=validate_all_fields,
                      skip_validation=skip_validation)
    return self


def delete(self: JObject) -> JObject:
    """Delete this object from database and clear linked relationships with
    delete rule.
    """
    self._can_delete_check()
    self._run_on_delete_callbacks()
    self._orm_delete()
    return self


def restore(self: JObject) -> JObject:
    """Restore this object from database and setup lost relationships with
    delete rule.
    """
    self._orm_restore()
    return self


def complete(self: JObject) -> JObject:
    """Fetch missing field values from the underlying ORM.
    """
    if self.is_partial:
        saved_modified_fields = list(self._modified_fields)
        saved_is_modified = self._is_modified
        self._orm_complete()
        self._is_modified = saved_is_modified
        self._modified_fields = saved_modified_fields
    return self


def _orm_complete(self: JObject) -> JObject:
    """ORM method override. Fetch missing field values and assign to this object.
    """
    pass


@property
def _data_dict(self: JObject) -> dict[str, Any]:
    """A dict which is a subview of __dict__ that only contains public data
    field items.
    """
    retval = {}
    for k, v in self.__dict__.items():
        if not k.startswith('_'):
            if k not in self._local_keys:
                retval[k] = v
    return retval


def _mark_new(self: JObject) -> None:
    """Mark the jsonclass object as a new object."""
    setattr(self, '_is_new', True)
    setattr(self, '_is_modified', False)
    setattr(self, '_modified_fields', set())
    setattr(self, '_previous_values', {})


def _mark_unmodified(self: JObject) -> None:
    """Mark this jsonclass object as an unmodified object."""
    setattr(self, '_is_new', False)
    setattr(self, '_is_modified', False)
    setattr(self, '_modified_fields', set())
    setattr(self, '_previous_values', {})


def _set_initial_status(self: JObject) -> None:
    """Set the initial status of the JSON class object."""
    self._mark_new()
    setattr(self, '_is_partial', False)
    setattr(self, '_is_deleted', False)
    setattr(self, '_previous_values', {})
    setattr(self, '_local_keys', set())
    setattr(self, '_local_key_map', {})
    setattr(self, '_unlinked_objects', {})
    setattr(self, '_link_keys', {})
    setattr(self, '_unlink_keys', {})
    setattr(self, '_graph', OGraph())
    setattr(self, '_operator', None)


def _mark_not_new(self: JObject) -> None:
    """Mark the jsonclass object as not a new object."""
    setattr(self, '_is_new', False)


def _add_link_key(self: JObject, fname: str, key: str | int) -> None:
    if self._link_keys.get(fname) is None:
        self._link_keys[fname] = []
    self._link_keys[fname].append(key)


def _add_unlink_key(self: JObject, fname: str, key: str | int) -> None:
    if self._unlink_keys.get(fname) is None:
        self._unlink_keys[fname] = []
    self._unlink_keys[fname].append(key)


def _add_unlinked_object(self: JObject,
                         field_name: str,
                         obj: JObject) -> None:
    """Add an object into unlinked objects pool."""
    if not self._unlinked_objects.get(field_name):
        self._unlinked_objects[field_name] = []
    if obj not in self._unlinked_objects[field_name]:
        self._unlinked_objects[field_name].append(obj)


def _del_unlinked_object(self: JObject,
                         field_name: str,
                         obj: JObject) -> None:
    """Remove an object from unlinked objects pool."""
    if not self._unlinked_objects.get(field_name):
        self._unlinked_objects[field_name] = []
    if obj in self._unlinked_objects[field_name]:
        self._unlinked_objects[field_name].remove(obj)


def _clear_unlinked_object(self: JObject) -> None:
    """Clear and reset all unlinked objects."""
    self._unlinked_objects = {}


def _set_on_save(self: JObject) -> None:
    """Update fields with setonsave marks if this object is modified. This
    is a graph operation. Objects chained with the saving object will also
    get setonsave called and saved.
    """
    modifier = InstanceOfModifier(self.__class__)
    ctx = Ctx.rootctx(self, CtxCfg())
    modifier.serialize(ctx)


def _clear_temp_fields(self: JObject) -> None:
    for field in self.__class__.cdef.fields:
        if field.fdef.fstore == FStore.TEMP:
            setattr(self, field.name, None)


def _database_write(self: JObject) -> None:
    pass


def _orm_delete(self: JObject) -> None:
    pass


def _orm_restore(self: JObject) -> None:
    pass


def _can_cu_check_common(self: JObject,
                         callbacks: list[Types | Callable],
                         action: str) -> None:
    if len(callbacks) == 0:
        return
    from .types import Types
    operator = getattr(self, '_operator')
    if operator is None:
        raise UnauthorizedActionException('no operator')
    for callback in callbacks:
        if isinstance(callback, Types):
            ctx = Ctx.rootctx(self, CtxCfg())
            tval = callback.modifier.transform(ctx)
            try:
                callback.modifier.validate(ctx.nval(tval))
            except ValidationException:
                raise UnauthorizedActionException(f'cannot {action}')
        else:
            result = callback(self, operator)
            if result is not None and result is not True:
                if isinstance(result, str):
                    raise UnauthorizedActionException(result)
                else:
                    raise UnauthorizedActionException(f'cannot {action}')


def _can_create_or_update_check(self: JObject) -> None:
    if self.is_new:
        self._can_cu_check_common(
            self.__class__.cdef.jconf.can_create, 'create')
    else:
        self._can_cu_check_common(
            self.__class__.cdef.jconf.can_update, 'update')


def _can_delete_check(self: JObject) -> None:
    self._can_cu_check_common(
        self.__class__.cdef.jconf.can_delete, 'delete')


def _can_read_check(self: JObject) -> None:
    self._can_cu_check_common(
        self.__class__.cdef.jconf.can_read, 'read')


def _run_on_create_callbacks(self: JObject) -> None:
    for callback in self.__class__.cdef.jconf.on_create:
        params_len = len(signature(callback).parameters)
        if params_len == 1:
            callback(self)
        else:
            callback(self, getattr(self, '_operator'))


def _run_on_update_callbacks(self: JObject) -> None:
    for callback in self.__class__.cdef.jconf.on_update:
        params_len = len(signature(callback).parameters)
        if params_len == 1:
            callback(self)
        else:
            callback(self, getattr(self, '_operator'))


def _run_on_delete_callbacks(self: JObject) -> None:
    for callback in self.__class__.cdef.jconf.on_delete:
        params_len = len(signature(callback).parameters)
        if params_len == 1:
            callback(self)
        else:
            callback(self, getattr(self, '_operator'))


@property
def _id(self: JObject) -> Union[str, int, None]:
    field = self.__class__.cdef.primary_field
    if not field:
        return None
    return getattr(self, field.name)


def __is_private_attr__(name: str) -> bool:
    """Returns true if the attribute name indicates private attribute."""
    return name.startswith('_')


def __setattr__(self: JObject, name: str, value: Any) -> None:
    # use original setattr for private fields
    if __is_private_attr__(name):
        self.__original_setattr__(name, value)
        return
    # use special method for local keys
    if name in self._local_keys:
        if value == getattr(self, name):
            return
        field_name = self._local_key_map[name]
        field = self.__class__.cdef.field_named(field_name)
        if field.fdef.ftype == FType.INSTANCE:
            if value is None:
                self.__original_setattr__(name, value)
                setattr(self, field_name, None)
            else:
                # temporarily set to none if key is modified
                # in the future, may query object from graph
                self.__original_setattr__(name, value)
                setattr(self, field_name, None)
        elif field.fdef.ftype == FType.LIST:
            olist = to_owned_list(self, value or [], name)
            self.__original_setattr__(name, olist)
            if (value is None) or (value is []):
                setattr(self, field_name, [])
            else:
                new_list = []
                curvals = getattr(self, field_name)
                if curvals is None:
                    curvals = []
                for item in value:
                    existitem = next((v for v in curvals if v._id == item), None)
                    if existitem is not None:
                        new_list.append(existitem)
                setattr(self, field_name, new_list)
        if not self.is_new:
            setattr(self, '_is_modified', True)
            self._modified_fields.add(field_name)
    # use original setattr for non JSON class fields
    try:
        field = self.__class__.cdef.field_named(name)
    except ValueError:
        self.__original_setattr__(name, value)
        return
    # this is a JSON class field attribute
    if field.fdef.fstore == FStore.CALCULATED:
        if field.fdef.setter is None:
            raise Exception('do not set to readonly calculation field')
        else:
            if callable(field.fdef.setter):
                field.fdef.setter(value, self)
            else:
                ctx = Ctx.rootctxp(self, name, None, value)
                field.fdef.setter.modifier.transform(ctx)
            return
    if hasattr(self, name) and value == getattr(self, name):
        return
    # track modified and previous value
    if not self.is_new:
        setattr(self, '_is_modified', True)
        self._modified_fields.add(name)
        if self.__class__.cdef.jconf.reset_all_fields or \
                field.fdef.has_reset_modifier:
            if name not in self.previous_values:
                self.previous_values[name] = getattr(self, name)
    # make list and dict assignments owned and monitored
    if isinstance(value, list):
        value = to_owned_list(self, value, name)
    if isinstance(value, dict):
        value = to_owned_dict(self, value, name)
    if field.fdef.is_ref:
        if hasattr(self, name):
            self.__unlink_field__(field, getattr(self, name))
        self.__original_setattr__(name, value)
        if field.fdef.fstore == FStore.LOCAL_KEY:
            rkes = self.__class__.cdef.jconf.ref_key_encoding_strategy
            rname = rkes(field)
            if field.fdef.ftype == FType.INSTANCE:
                if value is None:
                    self.__original_setattr__(rname, None)
                if isjsonobject(value):
                    self.__original_setattr__(rname, value._id)
            elif field.fdef.ftype == FType.LIST:
                if value is None:
                    olist = to_owned_list(self, [], rname)
                    self.__original_setattr__(rname, olist)
                else:
                    keys = []
                    for item in value:
                        if item is not None:
                            keys.append(item._id)
                    olist = to_owned_list(self, keys, rname)
                    self.__original_setattr__(rname, olist)
        self.__link_field__(field, value)
    else:
        self.__original_setattr__(name, value)


def __getattribute__(self: JObject, name: str, default: Any = None) -> Any:
    """This getattr takes calculated fields into account.
    """
    if name.startswith('_'):
        cls = getmro(type(self))[-2]
        return super(cls, self).__getattribute__(name)
    cdef = self.__class__.cdef
    if name in cdef.calc_field_names:
        getter = cdef.field_named(name).fdef.getter
        if callable(getter):
            return getter(self)
        else:
            ctx = Ctx.rootctx(self, CtxCfg(), self)
            return getter.modifier.transform(ctx)
    cls = getmro(type(self))[-2]
    return super(cls, self).__getattribute__(name)


def __odict_will_change__(self: JObject, odict: OwnedDict) -> None:
    # record previous value
    name = initial_keypath(odict.keypath)
    field = self.__class__.cdef.field_named(name)
    if self.__class__.cdef.jconf.reset_all_fields or \
            field.fdef.has_reset_modifier:
        if field.fdef.has_linked:
            return
        if name not in self.previous_values:
            if field.fdef.ftype == FType.DICT:
                self.previous_values[name] = unowned_copy_dict(
                    getattr(self, name))
            if field.fdef.ftype == FType.LIST:
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
    try:
        field = self.__class__.cdef.field_named(name)
    except:
        field = None
    if not field:
        return
    if self.__class__.cdef.jconf.reset_all_fields or \
            field.fdef.has_reset_modifier:
        if field.fdef.has_linked:
            return
        if name not in self.previous_values:
            if field.fdef.ftype == FType.DICT:
                self.previous_values[name] = unowned_copy_dict(
                    getattr(self, name))
            if field.fdef.ftype == FType.LIST:
                self.previous_values[name] = unowned_copy_list(
                    getattr(self, name))


def __olist_add__(self: JObject, olist: OwnedList, idx: int, val: Any) -> None:
    cdef = self.__class__.cdef
    if olist.keypath in self._local_keys:
        fname = self._local_key_map[olist.keypath]
        if not self._is_new and fname not in self._modified_fields:
            self._modified_fields.add(fname)
            self._is_modified = True
        return
    try:
        field = cdef.field_named(olist.keypath)
    except ValueError:
        field = None
    if field is not None and field.fdef.is_ref:
        self.__link_field__(field, [val])
        if field.fdef.fstore == FStore.LOCAL_KEY:
            rkes = cdef.jconf.ref_key_encoding_strategy
            rk = rkes(field)
            rlist = getattr(self, rk)
            if len(rlist) != len(olist):
                if val._id is None:
                    raise ValueError('a referenced object must have a valid primary key')
                rlist.insert(idx, val._id)
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


def __olist_del__(self: JObject, olist: OwnedList, val: Any) -> None:
    cdef = self.__class__.cdef
    if olist.keypath in self._local_keys:
        fname = self._local_key_map[olist.keypath]
        if not self._is_new and fname not in self._modified_fields:
            self._modified_fields.add(fname)
            self._is_modified = True
        flist = getattr(self, fname)
        if isinstance(flist, list):
            if len(flist) != len(olist):
                # TODO: reorder flist here
                # TODO: replace the underneath implementation
                match = next((v for v in flist if v._id == val), "PLACEHOLDER")
                if match != "PLACEHOLDER":
                    flist.remove(match)
        return
    try:
        field = cdef.field_named(olist.keypath)
    except ValueError:
        field = None
    if field and field.fdef.is_ref:
        self.__unlink_field__(field, [val])
        if field.fdef.fstore == FStore.LOCAL_KEY:
            ## TODO: replace the underneath implementation
            rkes = cdef.jconf.ref_key_encoding_strategy
            rk = rkes(field)
            rlist = getattr(self, rk)
            if len(rlist) != len(olist):
                if val is not None and val._id in rlist:
                    rlist.remove(val._id)
    # record modified
    if not self.is_new:
        setattr(self, '_is_modified', True)
        self._modified_fields.add(olist.keypath)


def __olist_sor__(self, olist: OwnedList) -> None:
    # TODO: sort local keys here
    # record modified
    if not self.is_new:
        setattr(self, '_is_modified', True)
        self._modified_fields.add(olist.keypath)


def __unlink_field__(self: JObject, field: JField, value: Any) -> None:
    items: list[JObject] = []
    if field.fdef.ftype == FType.INSTANCE:
        if not isjsonobject(value):
            return
        items = [value]
    if field.fdef.ftype == FType.LIST:
        if not isinstance(value, list):
            return
        items = list(value)
    for item in items:
        self._add_unlinked_object(field.name, item)
        other_field = field.foreign_field
        if other_field is None:
            return
        if other_field.fdef.ftype == FType.INSTANCE:
            if getattr(item, other_field.name) is self:
                item.__original_setattr__(other_field.name, None)
                of = other_field
                if of.fdef.fstore == FStore.LOCAL_KEY:
                    tsfm = item.__class__.cdef.jconf.ref_key_encoding_strategy
                    item.__original_setattr__(tsfm(other_field), None)
                    item._modified_fields.add(other_field.name)
                item._add_unlinked_object(other_field.name, self)
        elif other_field.fdef.ftype == FType.LIST:
            other_list = getattr(item, other_field.name)
            if isinstance(other_list, list):
                if self in other_list:
                    other_list.remove(self)
                    item._add_unlinked_object(other_field.name, self)


def __link_field__(self: JObject, field: JField, value: Any) -> None:
    items: list[JObject] = []
    if field.fdef.ftype == FType.INSTANCE:
        if not isjsonobject(value):
            return
        items = [value]
    if field.fdef.ftype == FType.LIST:
        if not isinstance(value, list):
            return
        items = value
    for item in items:
        self._del_unlinked_object(field.name, item)
        other_field = field.foreign_field
        if other_field is None:
            return
        if other_field.fdef.ftype == FType.INSTANCE:
            if getattr(item, other_field.name) != self:
                setattr(item, other_field.name, self)
                item._del_unlinked_object(other_field.name, self)
        elif other_field.fdef.ftype == FType.LIST:
            if not isinstance(getattr(item, other_field.name), list):
                setattr(item, other_field.name, [self])
                item._del_unlinked_object(other_field.name, self)
            else:
                if self not in getattr(item, other_field.name):
                    getattr(item, other_field.name).append(self)
                    item._del_unlinked_object(other_field.name, self)
        self.__link_graph__(item)


def __link_graph__(self: JObject, other: JObject) -> None:
    """
    """
    try:
        if not self._graph.has(self):
            self._graph.put(self)
    except UnlinkableJSONClassException:
        pass
    self._graph = self._graph.merged_graph(other._graph)


def jsonclassify(class_: type) -> type[JObject]:
    """Make a declared class into JSON class.

    Args:
        class_ (type): A class that user declared.

    Returns:
        JObject: A class that confirms to `JObject`.
    """
    # do not install methods for subclasses
    if hasattr(class_, '__is_jsonclass__'):
        return class_
    # type marks
    class_.__is_jsonclass__ = True
    # public methods
    class_.__init__ = __init__
    class_.set = jsonobject_set
    class_.update = update
    class_.tojson = tojson
    class_.validate = validate
    class_.is_valid = is_valid
    class_.opby = opby
    class_.is_new = is_new
    class_.is_modified = is_modified
    class_.is_partial = is_partial
    class_.is_deleted = is_deleted
    class_.modified_fields = modified_fields
    class_.persisted_modified_fields = persisted_modified_fields
    class_.previous_values = previous_values
    class_.unlinked_objects = unlinked_objects
    class_.reset = reset
    class_.save = save
    class_.delete = delete
    class_.restore = restore
    class_.complete = complete
    # protected methods
    class_._set = _set
    class_._keypath_set = _keypath_set
    class_._set_to_container = _set_to_container
    class_._orm_complete = _orm_complete
    class_._data_dict = _data_dict
    class_._mark_new = _mark_new
    class_._mark_unmodified = _mark_unmodified
    class_._set_initial_status = _set_initial_status
    class_._mark_not_new = _mark_not_new
    class_._add_link_key = _add_link_key
    class_._add_unlink_key = _add_unlink_key
    class_._add_unlinked_object = _add_unlinked_object
    class_._del_unlinked_object = _del_unlinked_object
    class_._clear_unlinked_object = _clear_unlinked_object
    class_._set_on_save = _set_on_save
    class_._clear_temp_fields = _clear_temp_fields
    class_._database_write = _database_write
    class_._orm_delete = _orm_delete
    class_._orm_restore = _orm_restore
    class_._can_cu_check_common = _can_cu_check_common
    class_._can_create_or_update_check = _can_create_or_update_check
    class_._can_delete_check = _can_delete_check
    class_._can_read_check = _can_read_check
    class_._run_on_create_callbacks = _run_on_create_callbacks
    class_._run_on_update_callbacks = _run_on_update_callbacks
    class_._run_on_delete_callbacks = _run_on_delete_callbacks
    class_._id = _id
    # private methods
    class_.__original_setattr__ = class_.__setattr__
    class_.__setattr__ = __setattr__
    class_.__getattribute__ = __getattribute__
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
