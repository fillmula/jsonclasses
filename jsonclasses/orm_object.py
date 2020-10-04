"""
This module contains `ORMObject`, the abstract base class for interacting with
ORMs.
"""
from __future__ import annotations
from typing import TypeVar, List
from .jsonclass import jsonclass
from .json_object import JSONObject


@jsonclass
class ORMObject(JSONObject):
    """This class provides common interface for integrating with ORMs. ORM
    integration authors should use defined fields of this class to provide an
    unified interface and usage.
    """

    @property
    def is_new(self) -> bool:
        if not hasattr(self, '_is_new'):
            self._is_new = True
        return self._is_new

    @property
    def is_modified(self) -> bool:
        if not hasattr(self, '_is_modified'):
            self._is_modified = False
        return self._is_modified

    @property
    def modified_fields(self) -> List[str]:
        if not hasattr(self, '_modified_fields'):
            self._modified_fields: List[str] = []
        return self._modified_fields


T = TypeVar('T', bound=ORMObject)
