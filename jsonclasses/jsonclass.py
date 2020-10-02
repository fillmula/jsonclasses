"""
This module contains `jsonclass`, the decorator for JSON Classes.
"""
from typing import Type, Optional, Union, TypeVar, overload, Callable, cast
from dataclasses import dataclass
from .json_object import JSONObject
from .graph import register_class
from .config import Config, LocalKey

T = TypeVar('T', bound=JSONObject)


@overload
def jsonclass(cls: Type[T]) -> Type[T]: ...


@overload
def jsonclass(
    cls: None,
    graph: Optional[str] = 'default',
    camelize_json_keys: Optional[bool] = None,
    camelize_db_keys: Optional[bool] = None,
    strict_input: Optional[bool] = None,
    primary_key: Optional[str] = None,
    local_key: Optional[LocalKey] = None
) -> Callable[[Type[T]], Type[T]]: ...


@overload
def jsonclass(
    cls: Type[T],
    graph: Optional[str] = 'default',
    camelize_json_keys: Optional[bool] = None,
    camelize_db_keys: Optional[bool] = None,
    strict_input: Optional[bool] = None,
    primary_key: Optional[str] = None,
    local_key: Optional[LocalKey] = None
) -> Type[T]: ...


def jsonclass(
    cls: Optional[Type[T]] = None,
    graph: Optional[str] = 'default',
    camelize_json_keys: Optional[bool] = None,
    camelize_db_keys: Optional[bool] = None,
    strict_input: Optional[bool] = None,
    primary_key: Optional[str] = None,
    local_key: Optional[LocalKey] = None
) -> Union[Callable[[Type[T]], Type[T]], Type[T]]:
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
            local_key=local_key
        )
        config.install_on_class(cls)
        return register_class(dataclass(init=False)(cls),
                              graph=cast(str, graph))
    else:
        def parametered_jsonclass(cls):
            return jsonclass(
                cls,
                graph=graph,
                camelize_json_keys=camelize_json_keys,
                camelize_db_keys=camelize_db_keys,
                strict_input=strict_input,
                primary_key=primary_key,
                local_key=local_key
            )
        return parametered_jsonclass
