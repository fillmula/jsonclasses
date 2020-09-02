import unittest
from jsonclasses import jsonclass, JSONObject, types
from datetime import datetime, date

class TestWriteonceValidator(unittest.TestCase):

  def test_writeonce_fields_cannot_be_updated_through_set_if_its_value_is_present(self):
    @jsonclass
    class User(JSONObject):
      nickname: str = types.str.required
      gender: str = types.str.writeonce.one_of(['male', 'female']).required
    user = User(nickname='Big Cock Brother', gender='male')
    user.set(**{ 'nickname': '20cm Brother', 'gender': 'female'})
    self.assertEqual(user.nickname, '20cm Brother')
    self.assertEqual(user.gender, 'male')

  def test_writeonce_fields_can_be_updated_through_set_if_its_value_is_not_present(self):
    @jsonclass
    class User(JSONObject):
      nickname: str = types.str.required
      gender: str = types.str.writeonce.one_of(['male', 'female']).required
    user = User(nickname='Alice')
    user.set(**{ 'nickname': 'Alice Heart', 'gender': 'female'})
    self.assertEqual(user.nickname, 'Alice Heart')
    self.assertEqual(user.gender, 'female')

  def test_writeonce_fields_can_be_updated_through_update_anyway(self):
    @jsonclass
    class User(JSONObject):
      nickname: str = types.str.required
      gender: str = types.str.writeonce.one_of(['male', 'female']).required
    user = User(nickname='Alice', gender='male')
    user.update(**{ 'nickname': 'Alice Heart', 'gender': 'female'})
    self.assertEqual(user.nickname, 'Alice Heart')
    self.assertEqual(user.gender, 'female')

  def test_writeonce_fields_can_be_updated_directly_anyway(self):
    @jsonclass
    class User(JSONObject):
      nickname: str = types.str.required
      gender: str = types.str.writeonce.one_of(['male', 'female']).required
    user = User(nickname='Alice', gender='male')
    user.gender = 'female'
    self.assertEqual(user.gender, 'female')
