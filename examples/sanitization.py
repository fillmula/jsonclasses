from jsonclasses import jsonclass, JSONObject, types

@jsonclass
class Coupon(JSONObject):
  type: str = types.str.oneof(['spring', 'flash', 'limited']).required
  discount_rate: float = types.float.range(0, 1).required
  used: bool = types.bool.readonly.default(False).required
  user_id: str = types.str.length(24).required

json_input = {
  'type': 'flash',
  'discount_rate': 0.3,
  'used': True,
  'user_id': '12345678901234567890abcd',
  'haha': 'I want to hack into this system!'
}

print(Coupon(**json_input))
