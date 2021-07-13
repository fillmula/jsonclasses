"""This module defines `Config`. Each JSON class has its own configuration. The
configuration object tweaks the behavior of JSON classes.
"""
from __future__ import annotations
from typing import Optional, Callable, Any, Union, cast, final, TYPE_CHECKING
from .jsonclass_object import JSONClassObject
if TYPE_CHECKING:
    from .jsonclass_field import JSONClassField
    from .jsonclass_graph import JSONClassGraph


OnCreate = Callable[[JSONClassObject, Any], None]
OnSave = Callable[[JSONClassObject, Any], None]
OnDelete = Callable[[JSONClassObject, Any], None]
CanCreate = Callable[[JSONClassObject, Any], Union[bool, None, str]]
CanUpdate = Callable[[JSONClassObject, Any], Union[bool, None, str]]
CanDelete = Callable[[JSONClassObject, Any], Union[bool, None, str]]
CanRead = Callable[[JSONClassObject, Any], Union[bool, None, str]]


@final
class Config:
    """The configuration of JSON classes. Each JSON class has its own
    configuration that each instance shares. This object tweaks the behavior of
    JSON classes.
    """

    def __init__(self: Config,
                 class_graph: Optional[str],
                 camelize_json_keys: Optional[bool],
                 strict_input: Optional[bool],
                 key_transformer: Optional[Callable[[JSONClassField], str]],
                 validate_all_fields: Optional[bool],
                 soft_delete: Optional[bool],
                 abstract: Optional[bool],
                 reset_all_fields: Optional[bool],
                 on_create: Optional[Union[OnCreate, list[OnCreate]]],
                 on_save: Optional[Union[OnSave, list[OnSave]]],
                 on_delete: Optional[Union[OnDelete, list[OnDelete]]],
                 can_create: Optional[Union[CanCreate, list[CanCreate]]],
                 can_update: Optional[Union[CanUpdate, list[CanUpdate]]],
                 can_delete: Optional[Union[CanDelete, list[CanDelete]]],
                 can_read: Optional[Union[CanRead, list[CanRead]]]) -> None:
        """
        Initialize a new configuration object.

        Args:
            class_graph (Optional[str]): The name of the class graph on which \
                the JSON class is defined.
            camelize_json_keys (Optional[bool]): Whether camelize keys when \
                outputing JSON.
            strict_input (Optional[bool]): Whether raise errors on receiving \
                invalid input keys.
            key_transformer (Optional[Callable[[JSONClassField], str]]): The \
                reference field local key conversion function.
            validate_all_fields (Optional[bool]): The default field \
                validating method when performing saving and validating.
            soft_delete (Optional[bool]): Whether perform soft delete on \
                deletion.
            abstract (Optional[bool]): Instance of abstract classes cannot \
                be initialized.
            reset_all_fields (Optional[bool]): Whether record all previous \
                values of an object and enable reset functionality.
            on_create (Optional[Union[OnCreate, list[OnCreate]]]): The callback
                on first time save.
            on_save (Optional[Union[OnSave, list[OnSave]]]): The callback on
                existing object save.
            on_delete (Optional[Union[OnDelete, list[OnDelete]]]): The callback
                on existing object deletion.
            can_create (Optional[Union[CanCreate, list[CanCreate]]]): The
                creation guard.
            can_update (Optional[Union[CanUpdate, list[CanUpdate]]]): The
                updation guard.
            can_delete (Optional[Union[CanDelete, list[CanDelete]]]): The
                deletion guard.
            can_read (Optional[Union[CanRead, list[CanRead]]]): The reading
                guard.
        """
        self._cls = None
        self._class_graph = class_graph or 'default'
        self._camelize_json_keys = camelize_json_keys
        self._strict_input = strict_input
        self._key_transformer = key_transformer
        self._validate_all_fields = validate_all_fields
        self._soft_delete = soft_delete
        self._abstract = abstract
        self._reset_all_fields = reset_all_fields
        if callable(on_create):
            self._on_create = [on_create]
        elif isinstance(on_create, list):
            self._on_create = on_create
        else:
            self._on_create = []
        if callable(on_save):
            self._on_save = [on_save]
        elif isinstance(on_save, list):
            self._on_save = on_save
        else:
            self._on_save = []
        if callable(on_delete):
            self._on_delete = [on_delete]
        elif isinstance(on_delete, list):
            self._on_delete = on_delete
        else:
            self._on_delete = []
        if callable(can_create):
            self._can_create = [can_create]
        elif isinstance(can_create, list):
            self._can_create = can_create
        else:
            self._can_create = []
        if callable(can_update):
            self._can_update = [can_update]
        elif isinstance(can_update, list):
            self._can_update = can_update
        else:
            self._can_update = []
        if callable(can_delete):
            self._can_delete = [can_delete]
        elif isinstance(can_delete, list):
            self._can_delete = can_delete
        else:
            self._can_delete = []
        if callable(can_read):
            self._can_read = [can_read]
        elif isinstance(can_read, list):
            self._can_read = can_read
        else:
            self._can_read = []

    def __eq__(self: Config, other: Any) -> bool:
        if not isinstance(other, Config):
            return False
        other_config = cast(Config, other)
        if self.class_graph != other_config.class_graph:
            return False
        if self.camelize_json_keys != other_config.camelize_json_keys:
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
        if self.on_create != other_config.on_create:
            return False
        if self.on_save != other_config.on_save:
            return False
        if self.on_delete != other_config._on_delete:
            return False
        if self.can_create != other_config.can_create:
            return False
        if self.can_update != other_config.can_update:
            return False
        if self.can_delete != other_config.can_delete:
            return False
        if self.can_read != other_config.can_read:
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

    @property
    def on_create(self: Config) -> list[OnCreate]:
        """The object creation callback.
        """
        return self._on_create

    @property
    def on_save(self: Config) -> list[OnSave]:
        """The object saving callback.
        """
        return self._on_save

    @property
    def on_delete(self: Config) -> list[OnDelete]:
        """The object deleting callback.
        """
        return self._on_delete

    @property
    def can_create(self: Config) -> list[CanCreate]:
        """The object creation guard.
        """
        return self._can_create

    @property
    def can_update(self: Config) -> list[CanUpdate]:
        """The object updation guard.
        """
        return self._can_update

    @property
    def can_delete(self: Config) -> list[CanDelete]:
        """The object deletion guard.
        """
        return self._can_delete

    @property
    def can_read(self: Config) -> list[CanRead]:
        """The object reading guard.
        """
        return self._can_read
