"""
This module contains `ORMObject`, the abstract base class for interacting with
ORMs.
"""
from __future__ import annotations
from jsonclasses.object_graph import ObjectGraph
from typing import TypeVar, Any
from .jsonclass import jsonclass
from .json_object import JSONObject
from .owned_dict import OwnedDict
from .owned_list import OwnedList
from .validators.instanceof_validator import InstanceOfValidator
from .contexts import TransformingContext


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

    def __setattr__(self: T, name: str, value: Any) -> None:
        # only mark modified fields for public properties
        if name[0] != '_' and not self.is_new:
            setattr(self, '_is_modified', True)
            self.modified_fields.add(name)
        super().__setattr__(name, value)

    def __odict_add__(self, odict: OwnedDict, key: str, val: Any) -> None:
        super().__odict_add__(odict, key, val)
        if not self.is_new:
            setattr(self, '_is_modified', True)
            self.modified_fields.add(odict.keypath)

    def __odict_del__(self, odict: OwnedDict, val: Any) -> None:
        super().__odict_del__(odict, val)
        if not self.is_new:
            setattr(self, '_is_modified', True)
            self.modified_fields.add(odict.keypath)

    def __olist_add__(self, olist: OwnedList, idx: int, val: Any) -> None:
        super().__olist_add__(olist, idx, val)
        if not self.is_new:
            setattr(self, '_is_modified', True)
            self.modified_fields.add(olist.keypath)

    def __olist_del__(self, olist: OwnedList, val: Any) -> None:
        super().__olist_del__(olist, val)
        if not self.is_new:
            setattr(self, '_is_modified', True)
            self.modified_fields.add(olist.keypath)

    def __olist_sor__(self, olist: OwnedList) -> None:
        super().__olist_sor__(olist)
        if not self.is_new:
            setattr(self, '_is_modified', True)
            self.modified_fields.add(olist.keypath)

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
    def modified_fields(self: T) -> set[str]:
        """The fields need to update the database record.
        """
        if not hasattr(self, '_modified_fields'):
            self._modified_fields: set[str] = set()
        return self._modified_fields

    @property
    def is_deleted(self: T) -> bool:
        """This property marks if the object is deleted from the database.
        """
        if not hasattr(self, '_is_deleted'):
            self._is_deleted = False
        return self._is_deleted

    def _setonsave(self: T) -> None:
        """Update fields with setonsave marks if this object is modified. This
        is a graph operation. Objects chained with the saving object will also
        get setonsave called and saved.
        """
        validator = InstanceOfValidator(self.__class__)
        config = self.__class__.config
        context = TransformingContext(
            value=self,
            keypath_root='',
            root=self,
            config_root=config,
            keypath_owner='',
            owner=self,
            config_owner=config,
            keypath_parent='',
            parent=self,
            fdesc=None,
            object_graph=ObjectGraph())
        validator.serialize(context)

    def _database_write(self: T) -> None:
        raise NotImplementedError('please override _database_write')

    def save(self: T,
             validate_all_fields: bool = False,
             skip_validation: bool = False) -> T:
        if not skip_validation:
            self.validate(all_fields=validate_all_fields)
        self._setonsave()
        self._database_write()
        return self


T = TypeVar('T', bound=ORMObject)
