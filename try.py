from jsonclasses import jsonclass, PersistableJsonObject, types

@jsonclass
class Color(PersistableJsonObject):
  red: int = types.int.range(0, 255).default(0).required
  green: int = types.int.range(0, 255).default(0).required
  blue: int = types.int.range(0, 255).default(0).required
  alpha: float = types.float.range(0, 1).default(1).required

network_input = { "red": 200, "green": 100, "unused": "我來搗亂哈哈" }
color = Color(**network_input)
print(color)
print(color.to_json())
