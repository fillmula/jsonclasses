from dataclasses import dataclass
from datetime import datetime
from .jsonclass import jsonclass
from .json_object import JsonObject

@jsonclass
class PersistableJsonObject(JsonObject):
  id: str
  created_at: datetime
  updated_at: datetime

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    now = datetime.now()
    if self.created_at is None:
      self.created_at = now
    if self.updated_at is None:
      self.updated_at = now

  def mark_updated(self):
    self.updated_at = datetime.now()
