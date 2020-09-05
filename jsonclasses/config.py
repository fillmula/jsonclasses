from __future__ import annotations
from typing import Optional, Type
from dataclasses import dataclass

camelize_json_keys = True
'''When initializing, setting values, updating values, and serializing,
whether automatically camelize json keys or not. Most of the times, JSON
keys are camelized since this is a data transfering format. Most of other
programming languages have camelized naming convensions. Python is an
exception. Use `config.camelize_json_keys = False` to disable this behavior
globally.
'''

camelize_db_keys = True
'''When integrating with ORMs, whether camelize keys and save to database.
'''

@dataclass
class Config:
  graph: str = 'default'
  camelize_json_keys: Optional[bool] = None
  camelize_db_keys: Optional[bool] = None

  def __post_init__(self):
    if self.camelize_json_keys is None:
      self.camelize_json_keys = camelize_json_keys
    if self.camelize_db_keys is None:
      self.camelize_db_keys = camelize_db_keys

  def install_on_class(self, cls: Type['JSONObject']):
    cls.config = self

  @classmethod
  def on(self, cls: type) -> Config:
    return cls.config
