from jsonclasses import jsonclass, JSONObject, types

@jsonclass
class MobilePhone(JSONObject):
  name: str = types.str.maxlength(50).required,
  model: str = types.str.oneof(['iphone', 'galaxy', 'pixel']).required,
  year: int = types.int.range(2010, 2020).required

mobile_phone = MobilePhone(name='iPhone 12', model='iphone', year=2020)

print(mobile_phone.tojson())
