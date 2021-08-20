"""
This module contains `jsonclass`, the decorator for JSON Classes.
"""
from typing import Optional, Union, Callable, overload, cast
from dataclasses import dataclass
from .jconf import (JConf, OnCreate, OnSave, CanCreate, OnDelete, CanUpdate,
                     CanDelete, CanRead)
from .jfield import JField
from .cdef import Cdef
from .jsonclassify import jsonclassify
from .jobject import JObject


@overload
def jsonclass(cls: type) -> type: ...


@overload
def jsonclass(
    cls: None,
    cgraph: Optional[str] = 'default',
    camelize_json_keys: Optional[bool] = None,
    strict_input: Optional[bool] = None,
    key_transformer: Optional[Callable[[JField], str]] = None,
    validate_all_fields: Optional[bool] = None,
    soft_delete: Optional[bool] = None,
    abstract: Optional[bool] = None,
    reset_all_fields: Optional[bool] = None,
    on_create: Optional[Union[OnCreate, list[OnCreate]]] = None,
    on_save: Optional[Union[OnSave, list[OnSave]]] = None,
    on_delete: Optional[Union[OnDelete, list[OnDelete]]] = None,
    can_create: Optional[Union[CanCreate, list[CanCreate]]] = None,
    can_update: Optional[Union[CanUpdate, list[CanUpdate]]] = None,
    can_delete: Optional[Union[CanDelete, list[CanDelete]]] = None,
    can_read: Optional[Union[CanRead, list[CanRead]]] = None,
) -> Callable[[type], type[JObject]]: ...


@overload
def jsonclass(
    cls: type,
    cgraph: Optional[str] = 'default',
    camelize_json_keys: Optional[bool] = None,
    strict_input: Optional[bool] = None,
    key_transformer: Optional[Callable[[JField], str]] = None,
    validate_all_fields: Optional[bool] = None,
    soft_delete: Optional[bool] = None,
    abstract: Optional[bool] = None,
    reset_all_fields: Optional[bool] = None,
    on_create: Optional[Union[OnCreate, list[OnCreate]]] = None,
    on_save: Optional[Union[OnSave, list[OnSave]]] = None,
    on_delete: Optional[Union[OnDelete, list[OnDelete]]] = None,
    can_create: Optional[Union[CanCreate, list[CanCreate]]] = None,
    can_update: Optional[Union[CanUpdate, list[CanUpdate]]] = None,
    can_delete: Optional[Union[CanDelete, list[CanDelete]]] = None,
    can_read: Optional[Union[CanRead, list[CanRead]]] = None,
) -> type[JObject]: ...


def jsonclass(
    cls: Optional[type] = None,
    cgraph: Optional[str] = 'default',
    camelize_json_keys: Optional[bool] = None,
    strict_input: Optional[bool] = None,
    key_transformer: Optional[Callable[[JField], str]] = None,
    validate_all_fields: Optional[bool] = None,
    soft_delete: Optional[bool] = None,
    abstract: Optional[bool] = None,
    reset_all_fields: Optional[bool] = None,
    on_create: Optional[Union[OnCreate, list[OnCreate]]] = None,
    on_save: Optional[Union[OnSave, list[OnSave]]] = None,
    on_delete: Optional[Union[OnDelete, list[OnDelete]]] = None,
    can_create: Optional[Union[CanCreate, list[CanCreate]]] = None,
    can_update: Optional[Union[CanUpdate, list[CanUpdate]]] = None,
    can_delete: Optional[Union[CanDelete, list[CanDelete]]] = None,
    can_read: Optional[Union[CanRead, list[CanRead]]] = None,
) -> Union[Callable[[type], type[JObject]], type[JObject]]:
    """The jsonclass object class decorator. To declare a jsonclass class, use
    this syntax:

      @jsonclass
      class MyObject:
        my_field_one: str
        my_field_two: bool
    """
    if cls is not None:
        if not isinstance(cls, type):
            raise ValueError('@jsonclass should be used to decorate a class.')
        jconf = JConf(
            cgraph=cast(str, cgraph),
            camelize_json_keys=camelize_json_keys,
            strict_input=strict_input,
            key_transformer=key_transformer,
            validate_all_fields=validate_all_fields,
            soft_delete=soft_delete,
            abstract=abstract,
            reset_all_fields=reset_all_fields,
            on_create=on_create,
            on_save=on_save,
            on_delete=on_delete,
            can_create=can_create,
            can_update=can_update,
            can_delete=can_delete,
            can_read=can_read)
        dcls: type = dataclass(init=False)(cls)
        jcls = jsonclassify(dcls)
        cdef = Cdef(jcls, jconf)
        jcls.cdef = cdef
        jconf.cgraph.put(cdef)
        return jcls
    else:
        def parametered_jsonclass(cls):
            return jsonclass(
                cls,
                cgraph=cgraph,
                camelize_json_keys=camelize_json_keys,
                strict_input=strict_input,
                key_transformer=key_transformer,
                validate_all_fields=validate_all_fields,
                soft_delete=soft_delete,
                abstract=abstract,
                reset_all_fields=reset_all_fields,
                on_create=on_create,
                on_save=on_save,
                on_delete=on_delete,
                can_create=can_create,
                can_update=can_update,
                can_delete=can_delete,
                can_read=can_read)
        return parametered_jsonclass
