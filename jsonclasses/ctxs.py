"""This module defines JSON Class context objects."""
from __future__ import annotations
from typing import Any, NamedTuple, Optional, Union, TYPE_CHECKING
from .mark_graph import MarkGraph
if TYPE_CHECKING:
    from .config import Config
    from .fdef import Fdef
    from .jobject import JObject


class VCtx(NamedTuple):
    """The context on which validating is performing. It contains necessary
    information for validators to validate the field values correctly.
    """
    value: Any
    keypath_root: str
    root: Any
    config_root: Config
    keypath_owner: str  # keypath relative to owner
    # the nearest json class instance or eager validation dict on which this
    # value is defined
    owner: Any
    config_owner: Config
    keypath_parent: Union[str, int]  # key relative to parent
    parent: Any  # the direct parent of this field
    fdef: Optional[Fdef] = None
    operator: Any = None
    all_fields: Optional[bool] = None
    mark_graph: MarkGraph = MarkGraph()

    def new(self, **kwargs):
        """Return a new validating context by replacing provided values."""
        keys = kwargs.keys()
        return VCtx(
            value=kwargs['value'] if 'value' in keys else self.value,
            keypath_root=(kwargs['keypath_root']
                          if 'keypath_root' in keys else self.keypath_root),
            root=kwargs['root'] if 'root' in keys else self.root,
            config_root=(kwargs['config_root']
                         if 'config_root' in keys else self.config_root),
            keypath_owner=(kwargs['keypath_owner']
                           if 'keypath_owner' in keys else self.keypath_owner),
            owner=kwargs['owner'] if 'owner' in keys else self.owner,
            config_owner=(kwargs['config_owner']
                          if 'config_owner' in keys else self.config_owner),
            keypath_parent=(kwargs['keypath_parent']
                            if 'keypath_parent' in keys
                            else self.keypath_parent),
            parent=kwargs['parent'] if 'parent' in keys else self.parent,
            fdef=(kwargs['fdef']
                        if 'fdef' in keys else self.fdef),
            operator=(kwargs['operator']
                      if 'operator' in keys else self.operator),
            all_fields=(kwargs['all_fields']
                        if 'all_fields' in keys else self.all_fields),
            mark_graph=(kwargs['mark_graph']
                        if 'mark_graph' in keys else self.mark_graph))

    def tctx(self):
        """Return a new transforming context by converting."""
        return TCtx(
            value=self.value,
            keypath_root=self.keypath_root,
            root=self.root,
            config_root=self.config_root,
            keypath_owner=self.keypath_owner,
            owner=self.owner,
            config_owner=self.config_owner,
            keypath_parent=self.keypath_parent,
            parent=self.parent,
            fdef=self.fdef,
            operator=self.operator,
            all_fields=self.all_fields,
            mark_graph=self.mark_graph)


class TCtx(NamedTuple):
    """The context on which transforming is performing. It contains necessary
    information for validators to transform the field values correctly.

    During transforming, eager validations are performed when needed. So all
    items from validating context are required for transforming.
    """
    value: Any
    keypath_root: str
    root: Any
    config_root: Config
    keypath_owner: str  # keypath relative to owner
    # the nearest json class instance or eager validation dict on which this
    # value is defined
    owner: Any
    config_owner: Config
    keypath_parent: Union[str, int]  # key relative to parent
    parent: Any  # the direct parent of this field
    fdef: Optional[Fdef] = None
    operator: Any = None
    all_fields: Optional[bool] = None
    dest: Optional[JObject] = None
    fill_dest_blanks: bool = True
    mark_graph: MarkGraph = MarkGraph()  # Override this, this is a placeholder

    def new(self, **kwargs):
        """Return a new transforming context by replacing provided values."""
        keys = kwargs.keys()
        return TCtx(
            value=kwargs['value'] if 'value' in keys else self.value,
            keypath_root=(kwargs['keypath_root']
                          if 'keypath_root' in keys else self.keypath_root),
            root=kwargs['root'] if 'root' in keys else self.root,
            config_root=(kwargs['config_root']
                         if 'config_root' in keys else self.config_root),
            keypath_owner=(kwargs['keypath_owner']
                           if 'keypath_owner' in keys else self.keypath_owner),
            owner=kwargs['owner'] if 'owner' in keys else self.owner,
            config_owner=(kwargs['config_owner']
                          if 'config_owner' in keys else self.config_owner),
            keypath_parent=(kwargs['keypath_parent']
                            if 'keypath_parent' in keys
                            else self.keypath_parent),
            parent=kwargs['parent'] if 'parent' in keys else self.parent,
            fdef=(kwargs['fdef']
                        if 'fdef' in keys else self.fdef),
            operator=(kwargs['operator']
                      if 'operator' in keys else self.operator),
            all_fields=(kwargs['all_fields']
                        if 'all_fields' in keys else self.all_fields),
            mark_graph=(kwargs['mark_graph']
                        if 'mark_graph' in keys else self.mark_graph))

    def vctx(self):
        """Return a new validating context by converting."""
        return VCtx(
            value=self.value,
            keypath_root=self.keypath_root,
            root=self.root,
            config_root=self.config_root,
            keypath_owner=self.keypath_owner,
            owner=self.owner,
            config_owner=self.config_owner,
            keypath_parent=self.keypath_parent,
            parent=self.parent,
            fdef=self.fdef,
            operator=self.operator,
            all_fields=self.all_fields,
            mark_graph=self.mark_graph)


class JCtx(NamedTuple):
    """The context on which `tojson` is performing. It contains necessary
    information for validators to convert the field values to JSON correctly.
    """
    value: Any
    config: Config
    fdef: Optional[Fdef] = None
    ignore_writeonly: bool = False
    entity_chain: list[str] = []  # for circular tojson strip duplicated refs

    def new(self, **kwargs):
        """Return a new tojson context by replacing provided values."""
        keys = kwargs.keys()
        return JCtx(
            value=kwargs['value'] if 'value' in keys else self.value,
            config=kwargs['config'] if 'config' in keys else self.config,
            fdef=(kwargs['fdef']
                        if 'fdef' in keys
                        else self.fdef),
            ignore_writeonly=(kwargs['ignore_writeonly']
                              if 'ignore_writeonly' in keys
                              else self.ignore_writeonly),
            entity_chain=(kwargs['entity_chain']
                          if 'entity_chain' in keys else self.entity_chain))
