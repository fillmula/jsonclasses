from __future__ import annotations
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

  def test_instanceof_validator_allow_argument_to_be_string(self):
    @jsonclass(graph='test_instanceof_7')
    class Post(JSONObject):
      title: str = types.str
      content: str = types.str
      author: User = types.instanceof('User')
    @jsonclass(graph='test_instanceof_7')
    class User(JSONObject):
      name: str = types.str
      posts: List[Post] = types.listof(types.instanceof('Post'))
    user = User(**{ 'name': 'John', 'posts': [
      { 'title': 'P1', 'content': 'C1' },
      { 'title': 'P2', 'content': 'C2' },
    ]})
    self.assertIs(user.posts[0].__class__, Post)
    self.assertIs(user.posts[1].__class__, Post)
    result = user.tojson()
    desired = {
      'name': 'John',
      'posts': [
        { 'title': 'P1', 'content': 'C1', 'author': None },
        { 'title': 'P2', 'content': 'C2', 'author': None }
      ]
    }
    self.assertEqual(result, desired)

  def test_instanceof_works_without_assigning_a_types(self):
    @jsonclass(graph='test_instanceof_8')
    class Staff(JSONObject):
      position: str
      user: User
    @jsonclass(graph='test_instanceof_8')
    class User(JSONObject):
      name: str = types.str
      staff: Staff
    user = User(**{ 'name': 'John', 'staff': { 'position': 'CEO' }})
    self.assertIsInstance(user.staff, Staff)
    self.assertEqual(user.staff.position, 'CEO')
    staff = Staff(**{ 'position': 'Developer', 'user': { 'name': 'Valy' }})
    self.assertIsInstance(staff.user, User)
    self.assertEqual(staff.user.name, 'Valy')

  def test_instanceof_works_in_list_without_assigning_a_types(self):
    @jsonclass(graph='test_instanceof_9')
    class Staff(JSONObject):
      position: str
      users: List[User]
    @jsonclass(graph='test_instanceof_9')
    class User(JSONObject):
      name: str
      staffs: List[Staff]
    user = User(**{ 'name': 'John', 'staffs': [{ 'position': 'CEO' }, { 'position': 'CSO' }]})
    self.assertIsInstance(user.staffs[0], Staff)
    self.assertEqual(user.staffs[0].position, 'CEO')
    staff = Staff(**{ 'position': 'Developer', 'users': [{ 'name': 'Valy' }, { 'name': 'Jonny' }]})
    self.assertIsInstance(staff.users[0], User)
    self.assertEqual(staff.users[0].name, 'Valy')

  def test_instanceof_works_in_dict_without_assigning_a_types(self):
    @jsonclass(graph='test_instanceof_10')
    class Staff(JSONObject):
      position: str
      users: Dict[str, User]
    @jsonclass(graph='test_instanceof_10')
    class User(JSONObject):
      name: str
      staffs: Dict[str,Staff]
    user = User(**{ 'name': 'John', 'staffs': { 'a': { 'position': 'CEO' }, 'b': { 'position': 'CSO' }}})
    self.assertIsInstance(user.staffs['a'], Staff)
    self.assertEqual(user.staffs['a'].position, 'CEO')
    staff = Staff(**{ 'position': 'Developer', 'users': { 'a': { 'name': 'Valy' }, 'b': { 'name': 'Jonny' }}})
    self.assertIsInstance(staff.users['a'], User)
    self.assertEqual(staff.users['a'].name, 'Valy')

  def test_instanceof_validates_in_list_without_assigning_a_types(self):
    @jsonclass(graph='test_instanceof_11')
    class Staff(JSONObject):
      position: str
      users: List[User]
    @jsonclass(graph='test_instanceof_11')
    class User(JSONObject):
      name: str
      staffs: List[Staff]
    user = User(**{ 'name': 'John', 'staffs': [{ 'position': 'CEO' }, None, { 'position': 'CSO' }]})
    with self.assertRaisesRegex(ValidationException, 'Value at \'staffs\\.1\' should not be None\\.'):
      user.validate()

  def test_instanceof_validates_in_dict_without_assigning_a_types(self):
    @jsonclass(graph='test_instanceof_12')
    class Staff(JSONObject):
      position: str
      users: Dict[str, User]
    @jsonclass(graph='test_instanceof_12')
    class User(JSONObject):
      name: str
      staffs: Dict[str, Staff]
    user = User(**{ 'name': 'John', 'staffs': { 'a': { 'position': 'CEO' }, 'b': None, 'c': { 'position': 'CSO' }}})
    with self.assertRaisesRegex(ValidationException, 'Value at \'staffs\\.b\' should not be None\\.'):
      user.validate()
