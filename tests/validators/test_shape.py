import unittest
from typing import Dict
from datetime import datetime, date
from jsonclasses import jsonclass, JSONObject, types
from jsonclasses.exceptions import ValidationException

class TestShapeValidator(unittest.TestCase):

  def test_shape_validator_validates_subfields(self):
    @jsonclass
    class User(JSONObject):
      address: dict = types.default({}).shape({
        'line1': types.str.required,
        'line2': types.str
      }).required
    user = User()
    self.assertRaisesRegex(ValidationException, '\'address\\.line1\' should not be None', user.validate)

  def test_shape_validator_do_not_throw_if_subfields_are_ok(self):
    @jsonclass
    class User(JSONObject):
      address: dict = types.default({}).shape({
        'line1': types.str.required,
        'line2': types.str
      }).required
    user = User(address={ 'line1': 'Shanghai' })
    try:
      user.validate()
    except:
      self.fail('shape validator should not throw if subfields are ok')

  def test_shape_validator_assigns_none_for_accessing(self):
    @jsonclass
    class User(JSONObject):
      address: dict = types.shape({
        'line1': types.str,
        'line2': types.str,
        'line3': types.str
      }).required
    user = User(address={ 'line1': 'Sydney' })
    self.assertEqual(user.__dict__, {
      'address': { 'line1': 'Sydney', 'line2': None, 'line3': None }
    })

  def test_shape_validator_sanitizes_input(self):
    @jsonclass
    class User(JSONObject):
      address: dict = types.shape({
        'line1': types.str,
        'line2': types.str,
        'line3': types.str
      }).required
    user = User(address={ 'line1': 'Sydney', 'haha': 'I\'m here' })
    self.assertEqual(user.__dict__, {
      'address': { 'line1': 'Sydney', 'line2': None, 'line3': None }
    })
