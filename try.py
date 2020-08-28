from jsonclasses import jsonclass, JsonObject, PersistableJsonObject

@jsonclass
class Point(PersistableJsonObject):
  x: float
  y: float

ddd = { "x": 2.5, "y": 3.6, "z": 7.8 }
point = Point(**ddd)
print(point)
print(point.to_json())
