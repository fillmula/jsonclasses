"""This module defines the `JField` named tuple. This data structure
records the detailed information of a JSON class field.
"""
from __future__ import annotations
from jsonclasses.jobject import JObject
from jsonclasses.fdef import FieldType
from typing import Any, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from .types import Types
    from .fdef import Fdef
    from .cdef import Cdef
    from .validators import ChainedValidator


class JField:
    """The detailed field information of a JSON class field. This includes
    field names in different circumstances, assigned default value, field
    description and main validator.
    """

    def __init__(
            self: JField, name: str, json_name: str, default: Any,
            types: Types, fdef: Fdef, validator: ChainedValidator) -> None:
        self._name = name
        self._json_name = json_name
        self._default = default
        self._types = types
        self._fdef = fdef
        self._validator = validator
        self._resolved_foreign = False
        self._foreign_cdef = None
        self._foreign_field = None
        self._foreign_fname = None
        self._resolved_foreign_class = False
        self._foreign_class = None

    @property
    def name(self: JField) -> str:
        """The name of the field in Python.
        """
        return self._name

    @property
    def json_name(self: JField) -> str:
        """The name of the field when converted into JSON dict.
        """
        return self._json_name

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
        return self._fdef

    @property
    def validator(self: JField) -> ChainedValidator:
        """The chained validator of the field.
        """
        return self._validator

    @property
    def foreign_cdef(self: JField) -> Optional[Cdef]:
        if self._resolved_foreign:
            return self._foreign_cdef
        self._resolve_foreign()
        return self._foreign_cdef

    @property
    def foreign_fname(self: JField) -> Optional[str]:
        if self._resolved_foreign:
            return self._foreign_fname
        self._resolve_foreign()
        return self._foreign_fname

    @property
    def foreign_field(self: JField) -> Optional[JField]:
        if self._resolved_foreign:
            return self._foreign_field
        self._resolve_foreign()
        return self._foreign_field

    @property
    def foreign_class(self: JField) -> Optional[type[JObject]]:
        if self._resolved_foreign_class:
            return self._foreign_class
        if self.fdef.field_type == FieldType.INSTANCE:
            self._foreign_class = self.fdef.inst_cls
        elif self.fdef.field_type == FieldType.LIST:
            self._foreign_class = self.fdef.item_types.fdef.inst_cls
        self._resolved_foreign_class = True
        return self._foreign_class

    def _resolve_foreign(self: JField) -> None:
        self._do_resolve_foreign()
        self._resolved_foreign = True

    def _do_resolve_foreign(self: JField) -> None:
        from .fdef import FieldStorage
        if self.fdef.field_storage not in [FieldStorage.LOCAL_KEY, FieldStorage.FOREIGN_KEY]:
            return None
        scls = self.fdef.cdef.cls
        slocal = self.fdef.field_storage == FieldStorage.LOCAL_KEY
        if self.fdef.field_type == FieldType.INSTANCE:
            fcls = self.foreign_class
            stype = 'inst'
        elif self.fdef.field_type == FieldType.LIST:
            fcls = self.foreign_class
            stype = 'list'
        self._foreign_cdef = fcls.cdef
        if slocal:
            ffield = fcls.cdef.rfield(scls, None, self.name)
            self._foreign_field = ffield
            self._foreign_fname = ffield.name
        else:
            fkey = self.fdef.foreign_key
            ffield = fcls.cdef.rfield(scls, fkey, None)
            self._foreign_field = ffield
            self._foreign_fname = ffield.name

        """Get the linked foreign field for local field named `name`.

        Args:
            name (str): The name of the local field.

        Returns:
            Optional[tuple[Cdef, str]]: A tuple which is a \
            combination of foreign class definition and foreign field name or \
            None if not found.

        Raises:
            LinkedFieldUnmatchException: A foreign field which is linked by \
            the field definition is found, however the properties don't match.
        """
