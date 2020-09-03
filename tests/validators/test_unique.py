import unittest
from jsonclasses import jsonclass, JSONObject, types
from jsonclasses.exceptions import ValidationException
from datetime import datetime, date

class TestUniqueValidator(unittest.TestCase):

  def test_unique_is_fine_when_create_an_object(self):
    @jsonclass
    class TestUser(JSONObject):
      password: str = types.str.writeonly.minlength(8).maxlength(16).transform(lambda p: p + '00xx').required
      phone_no: str
      username: str = types.str.writeonce.unique.required
      nickname: str = types.str.maxlength(30).required
      gender: str = types.str.writeonce.one_of(['male', 'female'])
      email: str = types.str.unique.required
    try:
      _user = TestUser()
    except ValidationException:
      self.fail('unique should not break things')
