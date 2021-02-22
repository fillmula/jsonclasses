"""This module defines utility functions for working with keypaths."""
from __future__ import annotations
from typing import TYPE_CHECKING
from .fields import FieldStorage, FieldType
if TYPE_CHECKING:
    from .jsonclass_field import JSONClassField


def reference_key(field: JSONClassField) -> str:
    """
    Figure out the correct reference key name from the field definition.

    Args:
        field (JSONClassField): The JSON class field to figure out reference
        key from.

    Returns:
        str: The reference key which represents this field.

    Raises:
        ValueError: ValueError is raised if the field definition is not a \
            supported reference field.
    """
    if field.definition.field_storage not in \
            [FieldStorage.FOREIGN_KEY, FieldStorage.LOCAL_KEY]:
        raise ValueError(f"field named {field.name} is not a reference field")
    if field.definition.field_type == FieldType.LIST:
        return field.name + '_ids'
    elif field.definition.field_type == FieldType.INSTANCE:
        return field.name + '_id'
    else:
        raise ValueError(f"field type {field.definition.field_type} is not a "
                         "supported reference field type")
