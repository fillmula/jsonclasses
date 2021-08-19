"""This module defines the `JField` named tuple. This data structure
records the detailed information of a JSON class field.
"""
from __future__ import annotations
from typing import NamedTuple, Any, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from .types import Types
    from .fdef import Fdef
    from .validators import ChainedValidator


class JField(NamedTuple):
    """The detailed field information of a JSON class field. This includes
    field names in different circumstances, assigned default value, field
    description and main validator.
    """

    name: str
    """The name of the field in Python.
    """

    json_name: str
    """The name of the field when converted into JSON dict.
    """

    default: Any
    """The default value that user assigned with equal sign.
    """

    types: Types
    """The user defined field types definition or auto generated types
    definition.
    """

    fdef: Fdef
    """The detailed field definition defined with the types chain.
    """

    validator: ChainedValidator
    """The chained validator of the field.
    """

    @property
    def foreign_field(self: JField) -> Optional[JField]:
        """The foreign field defined on the referenced object.
        """
        info = self.fdef.cdef.foreign_field_for(self.name)
        if info:
            foreign_cdef = info[0]
            foreign_field_name = info[1]
            return foreign_cdef.field_named(foreign_field_name)
        return None
