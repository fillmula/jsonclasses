from typing import Optional
from dataclasses import dataclass

camelize_json_keys = True
'''When initializing jsonclasses objects and setting jsonclasses object values,
handle key case style transforming or not.
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

  def install_on_class(self, cls: type):
    cls.config = self

  @classmethod
  def on(self, cls: type):
    return cls.config
