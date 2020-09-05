import unittest
from jsonclasses import jsonclass, JSONObject, types
from jsonclasses.exceptions import ValidationException

class TestJSONObjectValidate(unittest.TestCase):

  def test_validate_throws_if_object_is_not_valid(self):
    @jsonclass(graph='test_validate_1')
    class Contact(JSONObject):
      name: str = types.str.required
      address: str = types.str.required
    contact = Contact()
    self.assertRaises(ValidationException, contact.validate)

  def test_validate_does_not_throw_and_returns_self_if_object_is_valid(self):
    @jsonclass(graph='test_validate_2')
    class Name(JSONObject):
      first: str = types.str.required
      last: str = types.str.required
    name = Name(first='John', last='Range')
    self.assertEqual(name.validate(), name)

  def test_is_valid_returns_false_if_object_is_not_valid(self):
    @jsonclass(graph='test_validate_3')
    class Language(JSONObject):
      name: str = types.str.required
      code: str = types.str.required
    language = Language(name="English")
    self.assertEqual(language.is_valid(), False)

  def test_is_valid_returns_true_if_object_is_valid(self):
    @jsonclass(graph='test_validate_4')
    class Language(JSONObject):
      name: str = types.str.required
      code: str = types.str.required
    language = Language(name="English", code="en_US")
    self.assertEqual(language.is_valid(), True)

  def test_validate_validates_all_fields_if_with_all_fields_option_set_to_true(self):
    pass

  def test_validate_validates_until_it_found_an_invalid_field_with_all_fields_option_set_to_false(self):
    pass
