"""
This module contains `ORMObject`, the abstract base class for interacting with
ORMs.
"""
from __future__ import annotations
from typing import List, Any
from .jsonclass import jsonclass
from .json_object import JSONObject


@jsonclass
class ORMObject(JSONObject):
    """This class provides common interface for integrating with ORMs. ORM
    integration authors should use defined fields of this class to provide an
    unified interface and usage.
    """

    def __init__(self, **kwargs: Any) -> None:
        """Initialize a new ORM object object from keyed arguments or a dict.
        """
        super().__init__(**kwargs)
        setattr(self, '_is_modified', False)
        setattr(self, '_modified_fields', [])

    @property
    def is_new(self) -> bool:
        """This property marks if the object is newly created.
        """
        if not hasattr(self, '_is_new'):
            self._is_new = True
        return self._is_new

    @property
    def is_modified(self) -> bool:
        """This property marks if the object is modified and different with
        the database copy.
        """
        if not hasattr(self, '_is_modified'):
            self._is_modified = False
        return self._is_modified

    @property
    def modified_fields(self) -> List[str]:
        """The fields need to update the database record.
        """
        if not hasattr(self, '_modified_fields'):
            self._modified_fields: List[str] = []
        return self._modified_fields

    def __setattr__(self, name: str, value: Any) -> None:
        # only mark modified fields for public properties
        if name[0] != '_':
            setattr(self, '_is_modified', True)
            if name not in self.modified_fields:
                getattr(self, '_modified_fields').append(name)
        super().__setattr__(name, value)
