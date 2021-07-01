"""This module defines `JSONClassObject`, the protocol that JSON classes should
confirm to.
"""
from __future__ import annotations
from datetime import datetime
from typing import (Any, TypeVar, Optional, ClassVar, Protocol, Union,
                    TYPE_CHECKING)
if TYPE_CHECKING:
    from .class_definition import ClassDefinition
T = TypeVar('T', bound='JSONClassObject')


class JSONClassObject(Protocol):
    """The `JSONClassObject` protocol defines methods a qualified JSON class
    should implement.
    """

    definition: ClassVar[ClassDefinition]
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

    def tojson(self: T,
               ignore_writeonly: Optional[bool]) -> dict[str, Any]:
        """This tojson method returns a json dict representation of the JSON
        class object.
        """
        ...

    def validate(self: T, validate_all_fields: Optional[bool]) -> T:
        """This validate method validates the JSON class object. It raises if
        it's not valid.
        """
        ...

    def save(self: T,
             validate_all_fields: Optional[bool],
             skip_validation: Optional[bool]) -> T:
        """The save method saves the JSON class object into the persistent
        storage. Without a database decorator, this method raises.
        """
        ...

    def reset(self: T) -> T: ...

    def opby(self: T, operator: Any) -> T: ...

    @property
    def is_valid(self: T) -> bool: ...

    @property
    def is_new(self: T) -> bool: ...

    @property
    def is_modified(self: T) -> bool: ...

    @property
    def is_partial(self: T) -> bool: ...

    @property
    def is_deleted(self: T) -> bool: ...

    @property
    def is_outdated(self: T) -> bool: ...

    @property
    def modified_fields(self: T) -> set[str]: ...

    @property
    def persisted_modified_fields(self: T) -> set[str]: ...

    @property
    def previous_values(self: T) -> dict[str, Any]: ...

    @property
    def unlinked_objects(self: T) -> dict[str, list[T]]: ...

    def _mark_unmodified(self: T) -> None: ...

    def _clear_temp_fields(self: T) -> None: ...

    @property
    def _id(self: JSONClassObject) -> Union[str, int, None]: ...

    @property
    def _created_at(self: JSONClassObject) -> Optional[datetime]: ...

    @property
    def _updated_at(self: JSONClassObject) -> Optional[datetime]: ...

    @property
    def _deleted_at(self: JSONClassObject) -> Optional[datetime]: ...
