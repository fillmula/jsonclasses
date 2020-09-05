import unittest
from typing import List, Dict
from datetime import datetime, date
from jsonclasses import jsonclass, JSONObject, types
from jsonclasses.exceptions import ValidationException

class TestInstanceOfValidator(unittest.TestCase):

  def test_instanceof_validator_creates_instanceof_designated_class_on_transforming(self):
    @jsonclass(graph='test_instanceof_1')
    class Address(JSONObject):
      line1: str = types.str
      line2: str = types.str
    @jsonclass(graph='test_instanceof_1')
    class User(JSONObject):
      name: str = types.str
      address: Address = types.instanceof(Address)
    user = User(**{ 'name': 'John', 'address': { 'line1': 'London', 'line2': 'Road' }})
    self.assertIsInstance(user.address, Address)

  def test_instanceof_validator_validates_using_validator_inside(self):
    @jsonclass(graph='test_instanceof_2')
    class Address(JSONObject):
      line1: str = types.str.required
      line2: str = types.str
    @jsonclass(graph='test_instanceof_2')
    class User(JSONObject):
      name: str = types.str
      address: Address = types.instanceof(Address)
    user = User(**{ 'name': 'John', 'address': { 'line2': 'Road' }})
    self.assertRaisesRegex(ValidationException, 'Value at \'address\\.line1\' should not be None.', user.validate)

  def test_instanceof_validator_convert_subfields_to_json(self):
    @jsonclass(graph='test_instanceof_3')
    class Address(JSONObject):
      line1: str = types.str.required
      line2: str = types.str
    @jsonclass(graph='test_instanceof_3')
    class User(JSONObject):
      name: str = types.str
      address: Address = types.instanceof(Address)
    user = User(**{ 'name': 'John', 'address': { 'line2': 'Road', 'line1': 'OK' }})
    result = user.tojson()
    self.assertEqual(result, { 'name': 'John', 'address': { 'line1': 'OK', 'line2': 'Road' }})

  def test_instanceof_validator_creates_instances_inside_list(self):
    @jsonclass(graph='test_instanceof_4')
    class Address(JSONObject):
      line1: str = types.str
      line2: str = types.str
    @jsonclass(graph='test_instanceof_4')
    class User(JSONObject):
      name: str = types.str
      addresses: List[Address] = types.listof(types.instanceof(Address))
    user = User(**{ 'name': 'John', 'addresses': [
      { 'line1': 'London', 'line2': 'Road' },
      { 'line1': 'Paris', 'line2': 'Road' },
    ]})
    self.assertIsInstance(user.addresses[0], Address)
    self.assertIsInstance(user.addresses[1], Address)
    self.assertEqual(len(user.addresses), 2)
    self.assertEqual(user.addresses[0].__dict__, { 'line1': 'London', 'line2': 'Road' })
    self.assertEqual(user.addresses[1].__dict__, { 'line1': 'Paris', 'line2': 'Road' })

  def test_instanceof_validator_validates_instances_inside_list(self):
    @jsonclass(graph='test_instanceof_5')
    class Address(JSONObject):
      line1: str = types.str.required
      line2: str = types.str.required
    @jsonclass(graph='test_instanceof_5')
    class User(JSONObject):
      name: str = types.str
      addresses: List[Address] = types.listof(types.instanceof(Address))
    user = User(**{ 'name': 'John', 'addresses': [
      { 'line1': 'London' },
      { 'line1': 'Paris' },
    ]})
    self.assertRaises(ValidationException, user.validate)

  def test_instanceof_validator_converts_to_json_inside_list(self):
    @jsonclass(graph='test_instanceof_6')
    class Address(JSONObject):
      line1: str = types.str
      line2: str = types.str
    @jsonclass(graph='test_instanceof_6')
    class User(JSONObject):
      name: str = types.str
      addresses: List[Address] = types.listof(types.instanceof(Address))
    user = User(**{ 'name': 'John', 'addresses': [
      { 'line1': 'London', 'line2': 'Road' },
      { 'line1': 'Paris', 'line2': 'Road' },
    ]})
    result = user.tojson()
    desired = {'name': 'John', 'addresses': [{'line1': 'London', 'line2': 'Road'}, {'line1': 'Paris', 'line2': 'Road'}]}
    self.assertEqual(result, desired)
