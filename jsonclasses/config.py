"""This module contains JSON Class `config` aka configuration object."""
from __future__ import annotations
from typing import Optional, Type, TYPE_CHECKING
from dataclasses import dataclass
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


@dataclass
class Config:
    """The Config class contains user's settings for a JSON Class.
    """

    graph: str = 'default'
    camelize_json_keys: Optional[bool] = None
    camelize_db_keys: Optional[bool] = None
    linked_class: Optional[Type[JSONObject]] = None

    def __post_init__(self):
        if self.camelize_json_keys is None:
            self.camelize_json_keys = CAMELIZE_JSON_KEYS
        if self.camelize_db_keys is None:
            self.camelize_db_keys = CAMELIZE_DB_KEYS

    def install_on_class(self, cls: Type[JSONObject]):
        """Install config object onto a JSONObject class.
        """
        cls.config = self
        self.linked_class = cls

    @classmethod
    def on(cls, klass: Type[JSONObject]) -> Config:
        """Returns the config object attached to the class object.
        """
        return klass.config
