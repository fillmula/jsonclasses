import unittest
from jsonclasses import jsonclass, JSONObject, types
from jsonclasses.exceptions import ValidationException
from datetime import datetime, date

class TestEagerValidator(unittest.TestCase):

  def test_eager_validator_validates_on_init(self):
    @jsonclass
    class User(JSONObject):
      username: str = types.str.required
      password: str = types.str.minlength(8).maxlength(16).transform(lambda s: s + '0x0x').required
    with self.assertRaises(ValidationException) as context:
      _user = User(password='123')
      self.assertTrue("Value '123' at 'password' should have length not less than 8" in context.exception)

  def test_eager_validator_doesnt_cause_other_fields_to_validate_on_init(self):
    @jsonclass
    class User(JSONObject):
      username: str = types.str.required
      password: str = types.str.minlength(8).maxlength(10).transform(lambda s: s + '0x0x').required
    user = User(password='12345678')
    self.assertEqual(user.__dict__, { 'username': None, 'password': '123456780x0x' })

  def test_eager_validator_will_not_perform_when_value_is_none_on_init(self):
    @jsonclass
    class User(JSONObject):
      username: str = types.str.required
      password: str = types.str.minlength(8).maxlength(16).transform(lambda s: s + '0x0x').required
    try:
      _user = User()
    except ValidationException:
      self.fail('eager validator should not perform on init if value is None.')

  def test_eager_validator_validates_on_set(self):
    @jsonclass
    class User(JSONObject):
      username: str = types.str.required
      password: str = types.str.minlength(8).maxlength(16).transform(lambda s: s + '0x0x').required
    user = User()
    with self.assertRaises(ValidationException) as context:
      user.set(password='123')
      self.assertTrue("Value '123' at 'password' should have length not less than 8" in context.exception)

  def test_eager_validator_will_not_work_on_update(self):
    @jsonclass
    class User(JSONObject):
      username: str = types.str.required
      password: str = types.str.minlength(8).maxlength(16).transform(lambda s: s + '0x0x').required
    user = User()
    try:
      user.update(password='123')
    except ValidationException:
      self.fail('eager validator should not perform on update.')

  def test_eager_validator_prevents_validators_before_it_to_work_on_validate(self):
    @jsonclass
    class User(JSONObject):
      username: str = types.str.required
      password: str = types.str.minlength(2).maxlength(4).transform(lambda s: s + '0x0x').required
    user = User(username='john', password='1234')
    try:
      user.validate()
    except ValidationException:
      self.fail('eager validator should prevent validators before it to work on validate.')
