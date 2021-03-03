"""
This module contains `jsonclass`, the decorator for JSON Classes.
"""
from typing import Optional, Union, Callable, overload, cast
from dataclasses import dataclass
from .config import Config
from .jsonclass_field import JSONClassField
from .class_definition import ClassDefinition
from .jsonclassify import jsonclassify
from .jsonclass_object import JSONClassObject


@overload
def jsonclass(cls: type) -> type: ...


@overload
def jsonclass(
    cls: None,
    class_graph: Optional[str] = 'default',
    camelize_json_keys: Optional[bool] = None,
    camelize_db_keys: Optional[bool] = None,
    strict_input: Optional[bool] = None,
    key_transformer: Optional[Callable[[JSONClassField], str]] = None,
    validate_all_fields: Optional[bool] = None,
    soft_delete: Optional[bool] = None,
    abstract: Optional[bool] = None,
    reset_all_fields: Optional[bool] = None
) -> Callable[[type], type[JSONClassObject]]: ...


@overload
def jsonclass(
    cls: type,
    class_graph: Optional[str] = 'default',
    camelize_json_keys: Optional[bool] = None,
    camelize_db_keys: Optional[bool] = None,
    strict_input: Optional[bool] = None,
    key_transformer: Optional[Callable[[JSONClassField], str]] = None,
    validate_all_fields: Optional[bool] = None,
    soft_delete: Optional[bool] = None,
    abstract: Optional[bool] = None,
    reset_all_fields: Optional[bool] = None
) -> type[JSONClassObject]: ...


def jsonclass(
    cls: Optional[type] = None,
    class_graph: Optional[str] = 'default',
    camelize_json_keys: Optional[bool] = None,
    camelize_db_keys: Optional[bool] = None,
    strict_input: Optional[bool] = None,
    key_transformer: Optional[Callable[[JSONClassField], str]] = None,
    validate_all_fields: Optional[bool] = None,
    soft_delete: Optional[bool] = None,
    abstract: Optional[bool] = None,
    reset_all_fields: Optional[bool] = None
) -> Union[Callable[[type], type[JSONClassObject]], type[JSONClassObject]]:
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
        config = Config(
            class_graph=cast(str, class_graph),
            camelize_json_keys=camelize_json_keys,
            camelize_db_keys=camelize_db_keys,
            strict_input=strict_input,
            key_transformer=key_transformer,
            validate_all_fields=validate_all_fields,
            soft_delete=soft_delete,
            abstract=abstract,
            reset_all_fields=reset_all_fields)
        dataclass_cls = dataclass(init=False)(cls)
        jsonclass_cls = jsonclassify(dataclass_cls)
        definition = ClassDefinition(jsonclass_cls, config)
        cls.definition = definition
        config.class_graph.put(definition)
        return jsonclass_cls
    else:
        def parametered_jsonclass(cls):
            return jsonclass(
                cls,
                class_graph=class_graph,
                camelize_json_keys=camelize_json_keys,
                camelize_db_keys=camelize_db_keys,
                strict_input=strict_input,
                key_transformer=key_transformer,
                validate_all_fields=validate_all_fields,
                soft_delete=soft_delete,
                abstract=abstract,
                reset_all_fields=reset_all_fields)
        return parametered_jsonclass
