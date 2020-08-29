import unittest
from jsonclasses import jsonclass, JSONObject

class TestJSONObject(unittest.TestCase):

  def test_initialize_without_arguments(self):
    @jsonclass
    class Contact(JSONObject):
      name: str
      address: str
    contact = Contact()
    self.assertEqual(contact.__dict__, { 'name': None, 'address': None })

  def test_initialize_with_keyed_arguments(self):
    @jsonclass
    class BusinessCard(JSONObject):
      name: str
      phone_no: str
    card = BusinessCard(name='John', phone_no='012345678')
    self.assertEqual(card.__dict__, { 'name': 'John', 'phone_no': '012345678' })

  def test_initialize_with_keyed_arguments_fill_none_on_blank_keys(self):
    @jsonclass
    class Point(JSONObject):
      x: int
      y: int
    point = Point(x=50)
    self.assertEqual(point.__dict__, { 'x': 50, 'y': None })

  def test_initialize_with_keyed_arguments_remove_redundant_keys(self):
    @jsonclass
    class Size(JSONObject):
      width: float
      height: float
    size = Size(width=10.5, height=7.5, depth=2.5)
    self.assertEqual(size.__dict__, { 'width': 10.5, 'height': 7.5 })

  def test_initialize_with_a_dict(self):
    @jsonclass
    class Location(JSONObject):
      longitude: float
      latitude: float
    location = Location(**{ 'longitude': 0, 'latitude': 30 })
    self.assertEqual(location.__dict__, { 'longitude': 0, 'latitude': 30 })

  def test_initialize_with_dict_fill_none_on_blank_keys(self):
    @jsonclass
    class Point(JSONObject):
      x: int
      y: int
    input = { 'x': 50 }
    point = Point(**input)
    self.assertEqual(point.__dict__, { 'x': 50, 'y': None })

  def test_initialize_with_dict_remove_redundant_keys(self):
    @jsonclass
    class Size(JSONObject):
      width: float
      height: float
    input = { 'width': 10.5, 'height': 7.5, 'depth': 2.5 }
    size = Size(**input)
    self.assertEqual(size.__dict__, { 'width': 10.5, 'height': 7.5 })

  def test_initialize_fill_default_values_for_blank_keys(self):
    @jsonclass
    class Student(JSONObject):
      student_id: int = 5
      name: str = 'Student X'
    student = Student()
    self.assertEqual(student.__dict__, { 'student_id': 5, 'name': 'Student X' })

  def test_initialize_with_value_passed_in_rather_than_default_value(self):
    @jsonclass
    class Employee(JSONObject):
      no: int = 3
      name: str = 'Employee D'
    employee = Employee(no=20, name='John Larryson')
    self.assertEqual(employee.__dict__, { 'no': 20, 'name': 'John Larryson' })

if __name__ == '__main__':
    unittest.main()
