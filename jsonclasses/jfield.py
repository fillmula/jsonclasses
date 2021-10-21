"""This module defines the `JField` named tuple. This data structure
records the detailed information of a JSON class field.
"""
from __future__ import annotations
from jsonclasses.jobject import JObject
from jsonclasses.fdef import FType
from typing import Any, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from .types import Types
    from .fdef import Fdef
    from .cdef import Cdef
    from .modifiers import ChainedModifier


class JField:
    """The detailed field information of a JSON class field. This includes
    field names in different circumstances, assigned default value, field
    description and main modifier.
    """

    def __init__(
            self: JField, cdef: Cdef, name: str, default: Any,types: Types
        ) -> None:
        self._cdef = cdef
        self._name = name
        self._default = default
        self._types = types
        self._resolved_foreign = False
        self._foreign_cdef = None
        self._foreign_field = None
        self._foreign_fname = None
        self._resolved_foreign_class = False
        self._foreign_class = None

    @property
    def cdef(self: JField) -> Cdef:
        """The class definition on which this field is defined.
        """
        return self._cdef

    @property
    def name(self: JField) -> str:
        """The name of the field in Python.
        """
        return self._name

    @property
    def json_name(self: JField) -> str:
        """The name of the field when converted into JSON dict.
        """
        return self.cdef.jconf.key_encoding_strategy(self._name)

    @property
    def default(self: JField) -> Any:
        """The default value that user assigned with equal sign.
        """
        return self._default

    @property
    def types(self: JField) -> Types:
        """The user defined field types definition or auto generated types
        definition.
        """
        return self._types

    @property
    def fdef(self: JField) -> Fdef:
        """The detailed field definition defined with the types chain.
        """
        return self._types.fdef

    @property
    def modifier(self: JField) -> ChainedModifier:
        """The chained modifier of the field.
        """
        return self._types.modifier

    @property
    def foreign_cdef(self: JField) -> Optional[Cdef]:
        self.cdef._resolve_ref_types_if_needed()
        if self._resolved_foreign:
            return self._foreign_cdef
        self._resolve_foreign()
        return self._foreign_cdef

    @property
    def foreign_fname(self: JField) -> Optional[str]:
        self.cdef._resolve_ref_types_if_needed()
        if self._resolved_foreign:
            return self._foreign_fname
        self._resolve_foreign()
        return self._foreign_fname

    @property
    def foreign_field(self: JField) -> Optional[JField]:
        self.cdef._resolve_ref_types_if_needed()
        if self._resolved_foreign:
            return self._foreign_field
        self._resolve_foreign()
        return self._foreign_field

    @property
    def foreign_class(self: JField) -> Optional[type[JObject]]:
        self.cdef._resolve_ref_types_if_needed()
        if self._resolved_foreign_class:
            return self._foreign_class
        if self.fdef.ftype == FType.INSTANCE:
            self._foreign_class = self.fdef.inst_cls
        elif self.fdef.ftype == FType.LIST:
            self._foreign_class = self.fdef.item_types.fdef.inst_cls
        self._resolved_foreign_class = True
        return self._foreign_class

    def _resolve_foreign(self: JField) -> None:
        self._do_resolve_foreign()
        self._resolved_foreign = True

    def _do_resolve_foreign(self: JField) -> None:
        from .fdef import FStore
        if self.fdef.fstore not in [FStore.LOCAL_KEY, FStore.FOREIGN_KEY]:
            return None
        scls = self.fdef.cdef.cls
        slocal = self.fdef.fstore == FStore.LOCAL_KEY
        fcls = self.foreign_class
        if self.fdef.ftype == FType.INSTANCE:
            stype = 'inst'
        elif self.fdef.ftype == FType.LIST:
            stype = 'list'
        if not fcls:
            return
        self._foreign_cdef = fcls.cdef
        if slocal:
            ffield = fcls.cdef.rfield(scls, None, self.name)
            if ffield:
                self._foreign_field = ffield
                self._foreign_fname = ffield.name
        else:
            fkey = self.fdef.foreign_key
            ffield = fcls.cdef.rfield(scls, fkey, None)
            if ffield:
                self._foreign_field = ffield
                self._foreign_fname = ffield.name
