"""This module defines JSON Class context objects."""
from __future__ import annotations
from typing import Any, NamedTuple, TypeVar, Optional, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from .config import Config
    from .fields import FieldDescription
    from .json_object import JSONObject
    T = TypeVar('T', bound=JSONObject)


class ValidatingContext(NamedTuple):
    """The context on which validating is performing. It contains necessary
    information for validators to validate the field values correctly.
    """
    value: Any
    keypath: str
    root: Any
    config: Config
    keypath_owner: str  # keypath relative to owner
    owner: Any  # the nearest json class instance or eager validation dict on which this value is defined
    config_owner: Config
    keypath_parent: Union[str, int]  # key relative to parent
    parent: Any  # the direct parent of this field
    field_description: Optional[FieldDescription] = None
    all_fields: bool = True

    def new(self, **kwargs):
        keys = kwargs.keys()
        return ValidatingContext(
            value=kwargs['value'] if 'value' in keys else self.value,
            keypath=kwargs['keypath'] if 'keypath' in keys else self.keypath,
            root=kwargs['root'] if 'root' in keys else self.root,
            config=kwargs['config'] if 'config' in keys else self.config,
            keypath_owner=kwargs['keypath_owner'] if 'keypath_owner' in keys else self.keypath_owner,
            owner=kwargs['owner'] if 'owner' in keys else self.owner,
            config_owner=kwargs['config_owner'] if 'config_owner' in keys else self.config_owner,
            keypath_parent=kwargs['keypath_parent'] if 'keypath_parent' in keys else self.keypath_parent,
            parent=kwargs['parent'] if 'parent' in keys else self.parent,
            field_description=kwargs['field_description'] if 'field_description' in keys else self.field_description,
            all_fields=kwargs['all_fields'] if 'all_fields' in keys else self.all_fields)

    def transforming_context(self):
        return TransformingContext(
            value=self.value,
            keypath=self.keypath,
            root=self.root,
            config=self.config,
            keypath_owner=self.keypath_owner,
            owner=self.owner,
            config_owner=self.config_owner,
            keypath_parent=self.keypath_parent,
            parent=self.parent,
            field_description=self.field_description,
            all_fields=self.all_fields)


class TransformingContext(NamedTuple):
    """The context on which transforming is performing. It contains necessary
    information for validators to transform the field values correctly.

    During transforming, eager validations are performed when needed. So all
    items from validating context are required for transforming.
    """
    value: Any
    keypath: str
    root: Any
    config: Config
    keypath_owner: str  # keypath relative to owner
    owner: Any  # the nearest json class instance on which this value is defined
    config_owner: Config
    keypath_parent: Union[str, int]  # key relative to parent
    parent: Any  # the direct parent of this field
    field_description: Optional[FieldDescription] = None
    all_fields: bool = True
    dest: Optional[JSONObject] = None
    fill_dest_blanks: bool = True

    def new(self, **kwargs):
        keys = kwargs.keys()
        return TransformingContext(
            value=kwargs['value'] if 'value' in keys else self.value,
            keypath=kwargs['keypath'] if 'keypath' in keys else self.keypath,
            root=kwargs['root'] if 'root' in keys else self.root,
            config=kwargs['config'] if 'config' in keys else self.config,
            keypath_owner=kwargs['keypath_owner'] if 'keypath_owner' in keys else self.keypath_owner,
            owner=kwargs['owner'] if 'owner' in keys else self.owner,
            config_owner=kwargs['config_owner'] if 'config_owner' in keys else self.config_owner,
            keypath_parent=kwargs['keypath_parent'] if 'keypath_parent' in keys else self.keypath_parent,
            parent=kwargs['parent'] if 'parent' in keys else self.parent,
            field_description=kwargs['field_description'] if 'field_description' in keys else self.field_description,
            all_fields=kwargs['all_fields'] if 'all_fields' in keys else self.all_fields)

    def validating_context(self):
        return ValidatingContext(
            value=self.value,
            keypath=self.keypath,
            root=self.root,
            config=self.config,
            keypath_owner=self.keypath_owner,
            owner=self.owner,
            config_owner=self.config_owner,
            keypath_parent=self.keypath_parent,
            parent=self.parent,
            field_description=self.field_description,
            all_fields=self.all_fields)


class ToJSONContext(NamedTuple):
    """The context on which `tojson` is performing. It contains necessary
    information for validators to convert the field values to JSON correctly.
    """
    value: Any
    config: Config
    ignore_writeonly: bool = False

    def new(self, **kwargs):
        keys = kwargs.keys()
        return ToJSONContext(
            value=kwargs['value'] if 'value' in keys else self.value,
            config=kwargs['config'] if 'config' in keys else self.config,
            ignore_writeonly=kwargs['ignore_writeonly'] if 'ignore_writeonly' in keys else self.ignore_writeonly)
