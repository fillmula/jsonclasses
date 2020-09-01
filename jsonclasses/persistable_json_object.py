from datetime import datetime
from .jsonclass import jsonclass
from .json_object import JSONObject
from .types import types

@jsonclass
class PersistableJSONObject(JSONObject):
  '''This class provides common interface for integrating with ORMs.
  Additional fields in this class are id, created_at, and updated_at.
  '''

  id: str
  '''The id string of the object.
  '''

  created_at: datetime = types.datetime.default(lambda: datetime.now()).required
  '''This field records when this object is created.
  '''

  updated_at: datetime = types.datetime.default(lambda: datetime.now()).required
  '''This field records when this object is last updated.
  '''

  def set(self, fill_blanks=True, **kwargs):
    self._set(fill_blanks=False, **kwargs)
    self.updated_at = datetime.now()
    return self
