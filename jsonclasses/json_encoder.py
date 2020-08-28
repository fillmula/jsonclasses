from json.encoder import JSONEncoder as OldAndGrayJSONEncoder
from .json_object import JsonObject

class JSONEncoder(OldAndGrayJSONEncoder):
  def default(self, o):
    if isinstance(o, JsonObject):
      return o.to_json()
    else:
      return super().default(o)
