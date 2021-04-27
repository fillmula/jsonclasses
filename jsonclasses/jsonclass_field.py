"""This module defines the `JSONClassField` named tuple. This data structure
records the detailed information of a JSON class field.
"""
from __future__ import annotations
from typing import NamedTuple, Any, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from .types import Types
    from .field_definition import FieldDefinition
    from .validators import ChainedValidator


class JSONClassField(NamedTuple):
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

    definition: FieldDefinition
    """The detailed field definition defined with the types chain.
    """

    validator: ChainedValidator
    """The chained validator of the field.
    """

    @property
    def foreign_field(self: JSONClassField) -> Optional[JSONClassField]:
        """The foreign field defined on the referenced object.
        """
        info = self.definition.class_definition.foreign_field_for(self.name)
        if info:
            foreign_class_definition = info[0]
            foreign_field_name = info[1]
            return foreign_class_definition.field_named(foreign_field_name)
        return None
