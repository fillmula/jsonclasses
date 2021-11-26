"""This module defines `JConf`. Each JSON class has its own configuration. The
configuration object tweaks the behavior of JSON classes.
"""
from __future__ import annotations
from typing import Callable, Literal, Any, cast, final, TYPE_CHECKING
from .jobject import JObject
from .keypath import camelize_key, underscore_key, identical_key
if TYPE_CHECKING:
    from .jfield import JField
    from .cgraph import CGraph
    from .types import Types


OnCreate = Callable[[JObject, Any], None]
OnUpdate = Callable[[JObject, Any], None]
OnDelete = Callable[[JObject, Any], None]
CanCreate = Callable[[JObject, Any], bool | None | str]
CanUpdate = Callable[[JObject, Any], bool | None | str]
CanDelete = Callable[[JObject, Any], bool | None | str]
CanRead = Callable[[JObject, Any], bool | None | str]


@final
class JConf:
    """The configuration of JSON classes. Each JSON class has its own
    configuration that each instance shares. This object tweaks the behavior of
    JSON classes.
    """

    def __init__(self: JConf,
                 cgraph: str | None,
                 output_key_strategy: Callable[[str], str] | Literal['identical', 'camelize'] | None,
                 input_key_strategy: Callable[[str], str] | Literal['identical', 'underscore'] | None,
                 strict_input: bool | None,
                 ref_name_strategy: Callable[[JField], str] | None,
                 validate_all_fields: bool | None,
                 abstract: bool | None,
                 reset_all_fields: bool | None,
                 output_null: bool | None,
                 on_create: OnCreate | list[OnCreate] | Types | None,
                 on_update: OnUpdate | list[OnUpdate] | Types | None,
                 on_delete: OnDelete | list[OnDelete] | Types | None,
                 can_create: CanCreate | list[CanCreate] | Types | None,
                 can_update: CanUpdate | list[CanUpdate] | Types | None,
                 can_delete: CanDelete | list[CanDelete] | Types | None,
                 can_read: CanRead | list[CanRead] | Types | None) -> None:
        """
        Initialize a new configuration object.

        Args:
            cgraph (Optional[str]): The name of the class graph on which \
                the JSON class is defined.
            output_key_strategy (Optional[Callable[[str], str]]): How \
                object keys are encoded. The default is camelize.
            input_key_strategy (Optional[Callable[[str], str]]): How \
                object keys are decoded. The default is underscore.
            strict_input (Optional[bool]): Whether raise errors on receiving \
                invalid input keys.
            ref_name_strategy (Optional[Callable[[JField], str]]): The \
                reference field local key conversion function.
            validate_all_fields (Optional[bool]): The default field \
                validating method when performing saving and validating.
            abstract (Optional[bool]): Instance of abstract classes cannot \
                be initialized.
            reset_all_fields (Optional[bool]): Whether record all previous \
                values of an object and enable reset functionality.
            output_null: (Optional[bool]): Whether output null on tojson
                instead of leaving unexisting fields.
            on_create (Optional[Union[OnCreate, list[OnCreate]]]): The callback
                on first time save.
            on_update (Optional[Union[OnUpdate, list[OnUpdate]]]): The callback
                on existing object save.
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
        from .types import Types
        self._cls: type[JObject] | None = None
        self._cgraph = cgraph or 'default'
        self._output_key_strategy = _figure_out(output_key_strategy)
        self._input_key_strategy = _figure_out(input_key_strategy)
        self._strict_input = strict_input
        self._ref_name_strategy = ref_name_strategy
        self._validate_all_fields = validate_all_fields
        self._abstract = abstract
        self._reset_all_fields = reset_all_fields
        self._output_null = output_null
        if callable(on_create) or isinstance(on_create, Types):
            self._on_create = [on_create]
        elif isinstance(on_create, list):
            self._on_create = on_create
        else:
            self._on_create = []
        if callable(on_update) or isinstance(on_update, Types):
            self._on_update = [on_update]
        elif isinstance(on_update, list):
            self._on_update = on_update
        else:
            self._on_update = []
        if callable(on_delete) or isinstance(on_delete, Types):
            self._on_delete = [on_delete]
        elif isinstance(on_delete, list):
            self._on_delete = on_delete
        else:
            self._on_delete = []
        if callable(can_create) or isinstance(can_create, Types):
            self._can_create = [can_create]
        elif isinstance(can_create, list):
            self._can_create = can_create
        else:
            self._can_create = []
        if callable(can_update) or isinstance(can_update, Types):
            self._can_update = [can_update]
        elif isinstance(can_update, list):
            self._can_update = can_update
        else:
            self._can_update = []
        if callable(can_delete) or isinstance(can_delete, Types):
            self._can_delete = [can_delete]
        elif isinstance(can_delete, list):
            self._can_delete = can_delete
        else:
            self._can_delete = []
        if callable(can_read) or isinstance(can_read, Types):
            self._can_read = [can_read]
        elif isinstance(can_read, list):
            self._can_read = can_read
        else:
            self._can_read = []

    def __eq__(self: JConf, other: Any) -> bool:
        if not isinstance(other, JConf):
            return False
        other_config = cast(JConf, other)
        if self.cgraph != other_config.cgraph:
            return False
        if self.output_key_strategy != other_config.output_key_strategy:
            return False
        if self.input_key_strategy != other_config.input_key_strategy:
            return False
        if self.strict_input != other_config.strict_input:
            return False
        if self.ref_name_strategy != other_config.ref_name_strategy:
            return False
        if self.validate_all_fields != other_config.validate_all_fields:
            return False
        if self.abstract != other_config.abstract:
            return False
        if self.reset_all_fields != other_config.reset_all_fields:
            return False
        if self.output_null != other_config.output_null:
            return False
        if self.on_create != other_config.on_create:
            return False
        if self.on_update != other_config.on_update:
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
    def cls(self: JConf) -> type[JObject]:
        """The JSON class on which this class config is defined.
        """
        return cast(type[JObject], self._cls)

    @property
    def cgraph(self: JConf) -> CGraph:
        """The name of the class graph on which the JSON class is defined.
        """
        from .cgraph import CGraph
        return CGraph(self._cgraph)

    @property
    def output_key_strategy(self: JConf) -> Callable[[str], str]:
        """The object key encoding strategy.
        """
        if self._output_key_strategy is None:
            return self.cgraph.default_config.output_key_strategy
        return self._output_key_strategy

    @property
    def input_key_strategy(self: JConf) -> Callable[[str], str]:
        """The object key decoding strategy.
        """
        if self._input_key_strategy is None:
            return self.cgraph.default_config.input_key_strategy
        return self._input_key_strategy

    @property
    def strict_input(self: JConf) -> bool:
        """Whether raise errors on receiving invalid input keys.
        """
        if self._strict_input is None:
            return self.cgraph.default_config.strict_input
        return self._strict_input

    @property
    def ref_name_strategy(self: JConf) -> Callable[[JField], str]:
        """The reference field local key conversion function.
        """
        if self._ref_name_strategy is None:
            return self.cgraph.default_config.ref_name_strategy
        return self._ref_name_strategy

    @property
    def validate_all_fields(self: JConf) -> bool:
        """The default field validating method when performing saving and
        validating.
        """
        if self._validate_all_fields is None:
            return self.cgraph.default_config.validate_all_fields
        return self._validate_all_fields

    @property
    def abstract(self: JConf) -> bool:
        """Instance of abstract classes cannot be initialized.
        """
        if self._abstract is None:
            return self.cgraph.default_config.abstract
        return self._abstract

    @property
    def reset_all_fields(self: JConf) -> bool:
        """Whether record all previous values of an object and enable reset
        functionality.
        """
        if self._reset_all_fields is None:
            return self.cgraph.default_config.reset_all_fields
        return self._reset_all_fields

    @property
    def output_null(self: JConf) -> bool:
        """Whether output null values in the result json.
        """
        if self._output_null is None:
            return self.cgraph.default_config.output_null
        return self._output_null

    @property
    def on_create(self: JConf) -> list[OnCreate | Types]:
        """The object creation callback.
        """
        return self._on_create

    @property
    def on_update(self: JConf) -> list[OnUpdate | Types]:
        """The object saving callback.
        """
        return self._on_update

    @property
    def on_delete(self: JConf) -> list[OnDelete | Types]:
        """The object deleting callback.
        """
        return self._on_delete

    @property
    def can_create(self: JConf) -> list[CanCreate | Types]:
        """The object creation guard.
        """
        return self._can_create

    @property
    def can_update(self: JConf) -> list[CanUpdate | Types]:
        """The object updation guard.
        """
        return self._can_update

    @property
    def can_delete(self: JConf) -> list[CanDelete | Types]:
        """The object deletion guard.
        """
        return self._can_delete

    @property
    def can_read(self: JConf) -> list[CanRead | Types]:
        """The object reading guard.
        """
        return self._can_read


def _figure_out(s: Callable[[str], str] | Literal['identical', 'underscore', 'camelize'] | None) -> Callable[[str], str]:
    if s is None:
        return None
    if type(s) is str:
        match s:
            case 'underscore':
                return underscore_key
            case 'camelize':
                return camelize_key
            case _:
                return identical_key
    return s
