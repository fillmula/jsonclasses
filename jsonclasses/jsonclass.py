"""
This module contains `jsonclass`, the decorator for JSON Classes.
"""
from typing import Optional, Union, TypeVar, Callable, overload, cast
from dataclasses import dataclass
from .json_object import JSONObject
from .class_graph import class_graph_map
from .config import Config, LocalKey

T = TypeVar('T', bound=JSONObject)


@overload
def jsonclass(cls: type[T]) -> type[T]: ...


@overload
def jsonclass(
    cls: None,
    graph: Optional[str] = 'default',
    camelize_json_keys: Optional[bool] = None,
    camelize_db_keys: Optional[bool] = None,
    strict_input: Optional[bool] = None,
    primary_key: Optional[str] = None,
    local_key: Optional[LocalKey] = None,
    timestamps: Optional[list[str]] = None,
    validate_all_fields: Optional[bool] = None,
    soft_delete: Optional[bool] = None
) -> Callable[[type[T]], type[T]]: ...


@overload
def jsonclass(
    cls: type[T],
    graph: Optional[str] = 'default',
    camelize_json_keys: Optional[bool] = None,
    camelize_db_keys: Optional[bool] = None,
    strict_input: Optional[bool] = None,
    primary_key: Optional[str] = None,
    local_key: Optional[LocalKey] = None,
    timestamps: Optional[list[str]] = None,
    validate_all_fields: Optional[bool] = None,
    soft_delete: Optional[bool] = None
) -> type[T]: ...


def jsonclass(
    cls: Optional[type[T]] = None,
    graph: Optional[str] = 'default',
    camelize_json_keys: Optional[bool] = None,
    camelize_db_keys: Optional[bool] = None,
    strict_input: Optional[bool] = None,
    primary_key: Optional[str] = None,
    local_key: Optional[LocalKey] = None,
    timestamps: Optional[list[str]] = None,
    validate_all_fields: Optional[bool] = None,
    soft_delete: Optional[bool] = None
) -> Union[Callable[[type[T]], type[T]], type[T]]:
    """The jsonclass object class decorator. To declare a jsonclass class, use
    this syntax:

      @jsonclass
      class MyObject(JSONObject):
        my_field_one: str
        my_field_two: bool
    """
    if cls is not None:
        if not isinstance(cls, type):
            raise ValueError('@jsonclass should be used to decorate a class.')
        if not issubclass(cls, JSONObject):
            raise ValueError('@jsonclass should be used to decorate subclasses'
                             ' of JSONObject.')
        config = Config(
            graph=cast(str, graph),
            camelize_json_keys=camelize_json_keys,
            camelize_db_keys=camelize_db_keys,
            strict_input=strict_input,
            primary_key=primary_key,
            local_key=local_key,
            timestamps=timestamps,
            validate_all_fields=validate_all_fields,
            soft_delete=soft_delete)
        config.install_on_class(cls)
        dataclass_cls = dataclass(init=False)(cls)
        return class_graph_map.graph(cast(str, graph)).add(dataclass_cls)
    else:
        def parametered_jsonclass(cls):
            return jsonclass(
                cls,
                graph=graph,
                camelize_json_keys=camelize_json_keys,
                camelize_db_keys=camelize_db_keys,
                strict_input=strict_input,
                primary_key=primary_key,
                local_key=local_key,
                timestamps=timestamps,
                validate_all_fields=validate_all_fields,
                soft_delete=soft_delete)
        return parametered_jsonclass
