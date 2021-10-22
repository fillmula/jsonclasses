"""This module defines `JObject`, the protocol that JSON classes should
confirm to.
"""
from __future__ import annotations
from typing import (
    Any, Callable, TypeVar, Optional, ClassVar, Protocol, Set, TYPE_CHECKING
)
if TYPE_CHECKING:
    from .cdef import Cdef
    from .fdef import Fdef
    from .odict import OwnedDict
    from .olist import OwnedList
    from .jfield import JField
    from .types import Types
T = TypeVar('T', bound='JObject')


class JObject(Protocol):
    """The `JObject` protocol defines methods a qualified JSON class
    should implement.
    """

    cdef: ClassVar[Cdef]
    """The configuration user passed to JSON class through the jsonclass
    decorator.
    """

    def __init__(self: T, **kwargs: dict[str, Any]) -> None:
        """The initialization takes keyword arguments to initialize the field
        values of the object.
        """
        ...

    def set(self: T, **kwargs: dict[str, Any]) -> T:
        """The set method takes keyword arguments to update the field values of
        the object. Invalid fields are filtered. Eager validation are
        triggered. This is a safe method for accepting web inputs.
        """
        ...

    def update(self: T, **kwargs: dict[str, Any]) -> T:
        """The update method takes keyword arguments to update the field values
        of the object. Unlike `set`, the `update` method doesn't care about the
        validity of the values. This is an unsafe and internal updation method.
        """
        ...

    def tojson(self: T, ignore_writeonly: Optional[bool]) -> dict[str, Any]:
        """This tojson method returns a json dict representation of the JSON
        class object.
        """
        ...

    def validate(self: T, all_fields: Optional[bool]) -> T:
        """This validate method validates the JSON class object. It raises if
        it's not valid.
        """
        ...

    @property
    def is_valid(self: T) -> bool: ...

    def opby(self: T, operator: Any) -> T: ...

    @property
    def is_new(self: T) -> bool: ...

    @property
    def is_modified(self: T) -> bool: ...

    @property
    def is_partial(self: T) -> bool: ...

    @property
    def is_deleted(self: T) -> bool: ...

    @property
    def modified_fields(self: T) -> Set[str]: ...

    @property
    def persisted_modified_fields(self: T) -> Set[str]: ...

    @property
    def previous_values(self: T) -> dict[str, Any]: ...

    @property
    def unlinked_objects(self: T) -> dict[str, list[T]]: ...

    def reset(self: T) -> T: ...

    def save(self: T,
             validate_all_fields: Optional[bool] = None,
             skip_validation: Optional[bool] = None) -> T:
        """The save method saves the JSON class object into the persistent
        storage. Without a database decorator, this method raises.
        """
        ...

    def delete(self: T) -> T: ...

    def restore(self: T) -> T: ...

    def complete(self: T) -> T: ...

    def _set(self: T,
             kwargs: dict[str, Any],
             fill_blanks: Optional[bool]) -> None: ...

    def _keypath_set(self: T, kwargs: dict[str, Any]) -> None: ...

    def _set_to_container(self: JObject,
                      dest: Any,
                      items: list[str],
                      value: Any,
                      fdef: Fdef,
                      used_items: list[str]) -> None: ...

    def _orm_complete(self: T) -> None: ...

    @property
    def _data_dict(self: T) -> dict[str, Any]: ...

    def _mark_new(self: T) -> None: ...

    def _mark_unmodified(self: T) -> None: ...

    def _set_initial_status(self: T) -> None: ...

    def _mark_not_new(self: T) -> None: ...

    def _add_link_key(self: T, field_name: str, key: str | int): ...

    def _add_unlink_key(self: T, field_name: str, key: str | int): ...

    def _add_unlinked_object(self: T,
                             field_name: str,
                             obj: JObject) -> None: ...

    def _del_unlinked_object(self: T,
                             field_name: str,
                             obj: JObject) -> None: ...

    def _clear_unlinked_object(self: T) -> None: ...

    def _set_on_save(self: T) -> None: ...

    def _clear_temp_fields(self: T) -> None: ...

    def _database_write(self: T) -> None: ...

    def _orm_delete(self: T) -> None: ...

    def _orm_restore(self: T) -> None: ...

    def _can_cu_check_common(self: T,
                             callbacks: list[Callable | Types],
                             action: str) -> None: ...

    def _can_create_or_update_check(self: T) -> None: ...

    def _can_delete_check(self: T) -> None: ...

    def _can_read_check(self: T) -> None: ...

    def _run_on_create_callbacks(self: T) -> None: ...

    def _run_on_update_callbacks(self: T) -> None: ...

    def _run_on_delete_callbacks(self: T) -> None: ...

    @property
    def _id(self: T) -> str | int | None: ...

    @property
    def _operator(self: T) -> Optional[JObject]: ...

    def __original_setattr__(self: T, name: str, value: Any) -> None: ...

    def __setattr__(self: T, name: str, value: Any) -> None: ...

    def __getattribute__(self: T, name: str) -> None: ...

    def __odict_will_change__(self: T, odict: OwnedDict) -> None: ...

    def __odict_add__(self, odict: OwnedDict, key: str, val: Any) -> None: ...

    def __odict_del__(self, odict: OwnedDict, val: Any) -> None: ...

    def __olist_will_change__(self, olist: OwnedList) -> None: ...

    def __olist_add__(self: T,
                      olist: OwnedList,
                      idx: int,
                      val: Any) -> None: ...

    def __olist_del__(self: T, olist: OwnedList, val: Any) -> None: ...

    def __olist_sor__(self, olist: OwnedList) -> None: ...

    def __unlink_field__(self: T, field: JField, value: Any) -> None: ...

    def __link_field__(self: T, field: JField, value: Any) -> None: ...

    def __link_graph__(self: T, other: JObject) -> None: ...
