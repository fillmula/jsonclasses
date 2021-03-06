"""This module defines `Config`. Each JSON class has its own configuration. The
configuration object tweaks the behavior of JSON classes.
"""
from __future__ import annotations
from typing import Optional, Callable, Any, cast, final, TYPE_CHECKING
if TYPE_CHECKING:
    from .jsonclass_field import JSONClassField
    from .jsonclass_graph import JSONClassGraph
    from .jsonclass_object import JSONClassObject


@final
class Config:
    """The configuration of JSON classes. Each JSON class has its own
    configuration that each instance shares. This object tweaks the behavior of
    JSON classes.
    """

    def __init__(self: Config,
                 class_graph: Optional[str],
                 camelize_json_keys: Optional[bool],
                 camelize_db_keys: Optional[bool],
                 strict_input: Optional[bool],
                 key_transformer: Optional[Callable[[JSONClassField], str]],
                 validate_all_fields: Optional[bool],
                 soft_delete: Optional[bool],
                 abstract: Optional[bool],
                 reset_all_fields: Optional[bool]) -> None:
        """
        Initialize a new configuration object.

        Args:
            class_graph (Optional[str]): The name of the class graph on which \
                the JSON class is defined.
            camelize_json_keys (Optional[bool]): Whether camelize keys when \
                outputing JSON.
            camelize_db_keys (Optional[bool]): Whether camelize keys when \
                serializing into database.
            strict_input (Optional[bool]): Whether raise errors on receiving \
                invalid input keys.
            key_transformer (Optional[Callable[[JSONClassField], str]]): The \
                reference field local key conversion function.
            validate_all_fields (Optional[bool]): The default field \
                validating method when performing saving and validating.
            soft_delete (Optional[bool]): Whether perform soft delete on \
                deletion.
            abstract: (Optional[bool]): Instance of abstract classes cannot \
                be initialized.
            reset_all_fields: (Optional[bool]): Whether record all previous \
                values of an object and enable reset functionality.
        """
        self._cls = None
        self._class_graph = class_graph or 'default'
        self._camelize_json_keys = camelize_json_keys
        self._camelize_db_keys = camelize_db_keys
        self._strict_input = strict_input
        self._key_transformer = key_transformer
        self._validate_all_fields = validate_all_fields
        self._soft_delete = soft_delete
        self._abstract = abstract
        self._reset_all_fields = reset_all_fields

    def __eq__(self: Config, other: Any) -> bool:
        if not isinstance(other, Config):
            return False
        other_config = cast(Config, other)
        if self.class_graph != other_config.class_graph:
            return False
        if self.camelize_json_keys != other_config.camelize_json_keys:
            return False
        if self.camelize_db_keys != other_config.camelize_db_keys:
            return False
        if self.strict_input != other_config.strict_input:
            return False
        if self.key_transformer != other_config.key_transformer:
            return False
        if self.validate_all_fields != other_config.validate_all_fields:
            return False
        if self.soft_delete != other_config.soft_delete:
            return False
        if self.abstract != other_config.abstract:
            return False
        if self.reset_all_fields != other_config.reset_all_fields:
            return False
        return True

    @property
    def cls(self: Config) -> type[JSONClassObject]:
        """The JSON class on which this class config is defined.
        """
        return self._cls

    @property
    def class_graph(self: Config) -> JSONClassGraph:
        """The name of the class graph on which the JSON class is defined.
        """
        from .jsonclass_graph import JSONClassGraph
        return JSONClassGraph(self._class_graph)

    @property
    def camelize_json_keys(self: Config) -> bool:
        """Whether camelize keys when outputing JSON.
        """
        if self._camelize_json_keys is None:
            return self.class_graph.default_config.camelize_json_keys
        return self._camelize_json_keys

    @property
    def camelize_db_keys(self: Config) -> bool:
        """Whether camelize keys when serializing into database.
        """
        if self._camelize_db_keys is None:
            return self.class_graph.default_config.camelize_db_keys
        return self._camelize_db_keys

    @property
    def strict_input(self: Config) -> bool:
        """Whether raise errors on receiving invalid input keys.
        """
        if self._strict_input is None:
            return self.class_graph.default_config.strict_input
        return self._strict_input

    @property
    def key_transformer(self: Config) -> Callable[[JSONClassField], str]:
        """The reference field local key conversion function.
        """
        if self._key_transformer is None:
            return self.class_graph.default_config.key_transformer
        return self._key_transformer

    @property
    def validate_all_fields(self: Config) -> bool:
        """The default field validating method when performing saving and
        validating.
        """
        if self._validate_all_fields is None:
            return self.class_graph.default_config.validate_all_fields
        return self._validate_all_fields

    @property
    def soft_delete(self: Config) -> bool:
        """Whether perform soft delete on deletion.
        """
        if self._soft_delete is None:
            return self.class_graph.default_config.soft_delete
        return self._soft_delete

    @property
    def abstract(self: Config) -> bool:
        """Instance of abstract classes cannot be initialized.
        """
        if self._abstract is None:
            return self.class_graph.default_config.abstract
        return self._abstract

    @property
    def reset_all_fields(self: Config) -> bool:
        """Whether record all previous values of an object and enable reset
        functionality.
        """
        if self._reset_all_fields is None:
            return self.class_graph.default_config.reset_all_fields
        return self._reset_all_fields
