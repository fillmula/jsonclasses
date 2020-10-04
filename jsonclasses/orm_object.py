"""
This module contains `ORMObject`, the abstract base class for interacting with
ORMs.
"""
from __future__ import annotations
from typing import TypeVar, Set, Any
from .jsonclass import jsonclass
from .json_object import JSONObject


@jsonclass
class ORMObject(JSONObject):
    """This class provides common interface for integrating with ORMs. ORM
    integration authors should use defined fields of this class to provide an
    unified interface and usage.
    """

    def __init__(self: T, **kwargs: Any) -> None:
        """Initialize a new ORM object object from keyed arguments or a dict.
        """
        super().__init__(**kwargs)
        setattr(self, '_is_modified', False)
        setattr(self, '_modified_fields', set())

    @property
    def is_new(self: T) -> bool:
        """This property marks if the object is newly created.
        """
        if not hasattr(self, '_is_new'):
            self._is_new = True
        return self._is_new

    @property
    def is_modified(self: T) -> bool:
        """This property marks if the object is modified and different with
        the database copy.
        """
        if not hasattr(self, '_is_modified'):
            self._is_modified = False
        return self._is_modified

    @property
    def modified_fields(self: T) -> Set[str]:
        """The fields need to update the database record.
        """
        if not hasattr(self, '_modified_fields'):
            self._modified_fields: Set[str] = set()
        return self._modified_fields

    def __setattr__(self: T, name: str, value: Any) -> None:
        # only mark modified fields for public properties
        if name[0] != '_' and not self.is_new:
            setattr(self, '_is_modified', True)
            self.modified_fields.add(name)
        super().__setattr__(name, value)

    def mark_modified(self: T, *args: str) -> T:
        """Mark fields as modified.
        """
        if self.is_new:
            return self
        self.modified_fields.update(args)
        setattr(self, '_is_modified', True)
        return self


T = TypeVar('T', bound=ORMObject)
