"""
This module contains `jsonclass`, the decorator for JSON Classes.
"""
from __future__ import annotations
from jsonclasses.keypath import identical_key
from typing import Optional, Union, Callable, overload, cast, TYPE_CHECKING
from dataclasses import dataclass
from .jconf import (JConf, OnCreate, CanCreate, OnDelete, CanUpdate,
                     CanDelete, CanRead, OnUpdate)
from .jfield import JField
from .cdef import Cdef
from .jsonclassify import jsonclassify
from .jobject import JObject
if TYPE_CHECKING:
    from .types import Types


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
    on_create: OnCreate | list[OnCreate] | Types | None = None,
    on_update: OnUpdate | list[OnUpdate] | Types | None = None,
    on_delete: OnDelete | list[OnDelete] | Types | None = None,
    can_create: CanCreate | list[CanCreate] | Types | None = None,
    can_update: CanUpdate | list[CanUpdate] | Types | None = None,
    can_delete: CanDelete | list[CanDelete] | Types | None = None,
    can_read: CanRead | list[CanRead] | Types | None = None,
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
    on_create: OnCreate | list[OnCreate] | Types | None = None,
    on_update: OnUpdate | list[OnUpdate] | Types | None = None,
    on_delete: OnDelete | list[OnDelete] | Types | None = None,
    can_create: CanCreate | list[CanCreate] | Types | None = None,
    can_update: CanUpdate | list[CanUpdate] | Types | None = None,
    can_delete: CanDelete | list[CanDelete] | Types | None = None,
    can_read: CanRead | list[CanRead] | Types | None = None,
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
    on_create: OnCreate | list[OnCreate] | Types | None = None,
    on_update: OnUpdate | list[OnUpdate] | Types | None = None,
    on_delete: OnDelete | list[OnDelete] | Types | None = None,
    can_create: CanCreate | list[CanCreate] | Types | None = None,
    can_update: CanUpdate | list[CanUpdate] | Types | None = None,
    can_delete: CanDelete | list[CanDelete] | Types | None = None,
    can_read: CanRead | list[CanRead] | Types | None = None,
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
