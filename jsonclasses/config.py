"""This module contains JSON Class `config` aka configuration object."""
from __future__ import annotations
from typing import Optional, Callable, TYPE_CHECKING
from dataclasses import dataclass
from .fields import FieldType
if TYPE_CHECKING:
    from .json_object import JSONObject

CAMELIZE_JSON_KEYS = True
"""When initializing, setting values, updating values, and serializing,
whether automatically camelize json keys or not. Most of the times, JSON
keys are camelized since this is a data transfering format. Most of other
programming languages have camelized naming convensions. Python is an
exception. Use `config.CAMELIZE_JSON_KEYS = False` to disable this behavior
globally.
"""

CAMELIZE_DB_KEYS = True
"""When integrating with ORMs, whether camelize keys and save to database. This
is automatically on by default. Use `config.CAMELIZE_DB_KEYS = False` to
disable this behavior globally.
"""

STRICT_INPUT = True
"""When initializing JSON Class objects and set values, strict input classes
raises if invalid key value pairs are received.
"""

PRIMARY_KEY = 'id'
"""Instruct on how to find the primary key to this JSON Class objects.
"""

LocalKey = Callable[[str, FieldType], str]


def LOCAL_KEY(field_name: str, field_type: FieldType) -> str:
    """The default local_key resolve function."""
    if field_type == FieldType.LIST:
        return field_name + '_ids'
    return field_name + '_id'


TIMESTAMPS = ['created_at', 'updated_at', 'deleted_at']
"""The field names for timestamp fields. Specify None at specified position to
tell JSON Class that this class doesn't have that timestamp field.
"""

VALIDATE_ALL_FIELDS = True
"""When validating, if no validate rule specified, default to all fields.
"""

SOFT_DELETE = False
"""When deleting, if no delete rule specified, default to hard delete.
"""


@dataclass
class Config:
    """The Config class contains user's settings for a JSON Class.
    """

    class_graph: str = 'default'
    camelize_json_keys: Optional[bool] = None
    camelize_db_keys: Optional[bool] = None
    strict_input: Optional[bool] = None
    primary_key: Optional[str] = None
    local_key: Optional[LocalKey] = None
    timestamps: Optional[list[str]] = None
    validate_all_fields: Optional[bool] = None
    soft_delete: Optional[bool] = None

    linked_class: Optional[type[JSONObject]] = None

    def __post_init__(self):
        if self.camelize_json_keys is None:
            self.camelize_json_keys = CAMELIZE_JSON_KEYS
        if self.camelize_db_keys is None:
            self.camelize_db_keys = CAMELIZE_DB_KEYS
        if self.strict_input is None:
            self.strict_input = STRICT_INPUT
        if self.primary_key is None:
            self.primary_key = PRIMARY_KEY
        if self.local_key is None:
            self.local_key = LOCAL_KEY
        if self.timestamps is None:
            self.timestamps = TIMESTAMPS
        if self.validate_all_fields is None:
            self.validate_all_fields = VALIDATE_ALL_FIELDS
        if self.soft_delete is None:
            self.soft_delete = SOFT_DELETE

    def install_on_class(self, cls: type[JSONObject]):
        """Install config object onto a JSONObject class.
        """
        cls.config = self
        self.linked_class = cls
