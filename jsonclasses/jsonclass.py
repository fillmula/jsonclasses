"""
This module contains `jsonclass`, the decorator for JSON Classes.
"""
from jsonclasses.keypath import identical_key
from typing import Optional, Union, Callable, overload, cast
from dataclasses import dataclass
from .jconf import (JConf, OnCreate, CanCreate, OnDelete, CanUpdate,
                     CanDelete, CanRead, OnUpdate)
from .jfield import JField
from .cdef import Cdef
from .jsonclassify import jsonclassify
from .jobject import JObject


@overload
def jsonclass(cls: type) -> type[JObject]: ...


@overload
def jsonclass(
    cls: None = None,
    class_graph: Optional[str] = 'default',
    key_encoding_strategy: Optional[Callable[[str], str]] = None,
    key_decoding_strategy: Optional[Callable[[str], str]] = None,
    camelize_json_keys: Optional[bool] = None,
    strict_input: Optional[bool] = None,
    ref_key_encoding_strategy: Optional[Callable[[JField], str]] = None,
    validate_all_fields: Optional[bool] = None,
    abstract: Optional[bool] = None,
    reset_all_fields: Optional[bool] = None,
    on_create: Optional[Union[OnCreate, list[OnCreate]]] = None,
    on_update: Optional[Union[OnUpdate, list[OnUpdate]]] = None,
    on_delete: Optional[Union[OnDelete, list[OnDelete]]] = None,
    can_create: Optional[Union[CanCreate, list[CanCreate]]] = None,
    can_update: Optional[Union[CanUpdate, list[CanUpdate]]] = None,
    can_delete: Optional[Union[CanDelete, list[CanDelete]]] = None,
    can_read: Optional[Union[CanRead, list[CanRead]]] = None,
) -> Callable[[type], type[JObject]]: ...


@overload
def jsonclass(
    cls: type,
    class_graph: Optional[str] = 'default',
    key_encoding_strategy: Optional[Callable[[str], str]] = None,
    key_decoding_strategy: Optional[Callable[[str], str]] = None,
    camelize_json_keys: Optional[bool] = None,
    strict_input: Optional[bool] = None,
    ref_key_encoding_strategy: Optional[Callable[[JField], str]] = None,
    validate_all_fields: Optional[bool] = None,
    abstract: Optional[bool] = None,
    reset_all_fields: Optional[bool] = None,
    on_create: Optional[Union[OnCreate, list[OnCreate]]] = None,
    on_update: Optional[Union[OnUpdate, list[OnUpdate]]] = None,
    on_delete: Optional[Union[OnDelete, list[OnDelete]]] = None,
    can_create: Optional[Union[CanCreate, list[CanCreate]]] = None,
    can_update: Optional[Union[CanUpdate, list[CanUpdate]]] = None,
    can_delete: Optional[Union[CanDelete, list[CanDelete]]] = None,
    can_read: Optional[Union[CanRead, list[CanRead]]] = None,
) -> type[JObject]: ...


def jsonclass(
    cls: Optional[type] = None,
    class_graph: Optional[str] = 'default',
    key_encoding_strategy: Optional[Callable[[str], str]] = None,
    key_decoding_strategy: Optional[Callable[[str], str]] = None,
    camelize_json_keys: Optional[bool] = None,
    strict_input: Optional[bool] = None,
    ref_key_encoding_strategy: Optional[Callable[[JField], str]] = None,
    validate_all_fields: Optional[bool] = None,
    abstract: Optional[bool] = None,
    reset_all_fields: Optional[bool] = None,
    on_create: Optional[Union[OnCreate, list[OnCreate]]] = None,
    on_update: Optional[Union[OnUpdate, list[OnUpdate]]] = None,
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
        if camelize_json_keys is False:
            key_encoding_strategy = identical_key
            key_decoding_strategy = identical_key
        jconf = JConf(
            cgraph=cast(str, class_graph),
            key_encoding_strategy=key_encoding_strategy,
            key_decoding_strategy=key_decoding_strategy,
            strict_input=strict_input,
            ref_key_encoding_strategy=ref_key_encoding_strategy,
            validate_all_fields=validate_all_fields,
            abstract=abstract,
            reset_all_fields=reset_all_fields,
            on_create=on_create,
            on_update=on_update,
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
                class_graph=class_graph,
                key_encoding_strategy=key_encoding_strategy,
                key_decoding_strategy=key_decoding_strategy,
                camelize_json_keys=camelize_json_keys,
                strict_input=strict_input,
                ref_key_encoding_strategy=ref_key_encoding_strategy,
                validate_all_fields=validate_all_fields,
                abstract=abstract,
                reset_all_fields=reset_all_fields,
                on_create=on_create,
                on_update=on_update,
                on_delete=on_delete,
                can_create=can_create,
                can_update=can_update,
                can_delete=can_delete,
                can_read=can_read)
        return parametered_jsonclass
