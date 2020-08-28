from dataclasses import dataclass
from datetime import datetime
from .jsonclass import jsonclass
from .json_object import JsonObject
from .types import types

@jsonclass
class PersistableJsonObject(JsonObject):
  id: str
  created_at: datetime = types.datetime.default(datetime.now()).required
  updated_at: datetime = types.datetime.default(datetime.now()).required

  def mark_updated(self):
    self.updated_at = datetime.now()
