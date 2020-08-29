from datetime import datetime
from .jsonclass import jsonclass
from .json_object import JSONObject
from .types import types

@jsonclass
class PersistableJSONObject(JSONObject):

  id: str

  created_at: datetime = types.datetime.default(lambda: datetime.now()).required

  updated_at: datetime = types.datetime.default(lambda: datetime.now()).required

  def mark_updated(self):
    self.updated_at = datetime.now()
    return self
