from jsonclasses import jsonclass, JSONObject, types

@jsonclass
class UserProfile(JSONObject):
  name: str = types.str.required
  gender: str = types.str.oneof(['male', 'female'])

user_profile = UserProfile(name='John', gender='mlae')

user_profile.validate()
