import unittest
from typing import Dict
from datetime import datetime, date
from jsonclasses import jsonclass, JSONObject, types
from jsonclasses.exceptions import ValidationException

class TestInstanceOfValidator(unittest.TestCase):

  def test_instance_of_validator_creates_instance_of_designated_class_on_transforming(self):
    pass
    @jsonclass
    class Address(JSONObject):
      line1: str = types.str
      line2: str = types.str
    @jsonclass
    class User(JSONObject):
      name: str = types.str
      address: Address = types.instance_of(Address)
    user = User(**{ 'name': 'John', 'address': { 'line1': 'London', 'line2': 'Road' }})
    self.assertIsInstance(user.address, Address)

  def test_instance_of_validator_validates_using_validator_inside(self):
    @jsonclass
    class Address(JSONObject):
      line1: str = types.str.required
      line2: str = types.str
    @jsonclass
    class User(JSONObject):
      name: str = types.str
      address: Address = types.instance_of(Address)
    user = User(**{ 'name': 'John', 'address': { 'line2': 'Road' }})
    self.assertRaisesRegex(ValidationException, 'Value at \'address\\.line1\' should not be None.', user.validate)

  def test_instance_of_validator_convert_subfields_to_json(self):
    @jsonclass
    class Address(JSONObject):
      line1: str = types.str.required
      line2: str = types.str
    @jsonclass
    class User(JSONObject):
      name: str = types.str
      address: Address = types.instance_of(Address)
    user = User(**{ 'name': 'John', 'address': { 'line2': 'Road', 'line1': 'OK' }})
    result = user.tojson()
    self.assertEqual(result, { 'name': 'John', 'address': { 'line1': 'OK', 'line2': 'Road' }})
