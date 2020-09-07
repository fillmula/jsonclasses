from jsonclasses import jsonclass, JSONObject, types

@jsonclass
class User(JSONObject):
  phone_no: str = types.str.unique.index.match(local_phone_no_regex).required
  email: str = types.str.match(email_regex)
  password: str = types.str.length(8, 16).match(secure_password_regex).transform(salt).required
  nickname: str = types.str.required
  gender: str = types.str.writeonce.oneof(['male', 'female'])
  age: int = types.int.min(18).max(100)
  intro: str = types.str.maxlength(500)
