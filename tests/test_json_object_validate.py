import unittest
from typing import List, Dict
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
    @jsonclass(graph='test_validate_5')
    class Language(JSONObject):
      name: str = types.str.required
      code: str = types.str.required
    language = Language()
    with self.assertRaises(ValidationException) as context:
      language.validate()
    exception = context.exception
    self.assertTrue(len(exception.keypath_messages) == 2)
    self.assertRegex(exception.keypath_messages['name'], 'Value at \'name\' should not be None\\.')
    self.assertRegex(exception.keypath_messages['code'], 'Value at \'code\' should not be None\\.')

  def test_validate_validates_until_it_found_an_invalid_field_with_all_fields_option_set_to_false(self):
    @jsonclass(graph='test_validate_6')
    class Language(JSONObject):
      name: str = types.str.required
      code: str = types.str.required
    language = Language()
    with self.assertRaises(ValidationException) as context:
      language.validate(all_fields=False)
    exception = context.exception
    self.assertTrue(len(exception.keypath_messages) == 1)
    self.assertRegex(exception.keypath_messages['name'], 'Value at \'name\' should not be None\\.')

  def test_validate_validates_all_fields_inside_list(self):
    @jsonclass(graph='test_validate_7')
    class TestNumber(JSONObject):
      numbers: List[int] = types.listof(types.int.min(100))
    number = TestNumber(numbers=[1,2,3,4,5])
    with self.assertRaises(ValidationException) as context:
      number.validate()
    exception = context.exception
    self.assertTrue(len(exception.keypath_messages) == 5)
    self.assertRegex(exception.keypath_messages['numbers.0'], 'Value \'1\' at \'numbers\\.0\' should not be less than 100\\.')
    self.assertRegex(exception.keypath_messages['numbers.1'], 'Value \'2\' at \'numbers\\.1\' should not be less than 100\\.')
    self.assertRegex(exception.keypath_messages['numbers.2'], 'Value \'3\' at \'numbers\\.2\' should not be less than 100\\.')
    self.assertRegex(exception.keypath_messages['numbers.3'], 'Value \'4\' at \'numbers\\.3\' should not be less than 100\\.')
    self.assertRegex(exception.keypath_messages['numbers.4'], 'Value \'5\' at \'numbers\\.4\' should not be less than 100\\.')

  def test_validate_validates_only_one_field_inside_list(self):
    @jsonclass(graph='test_validate_8')
    class TestNumber(JSONObject):
      numbers: List[int] = types.listof(types.int.min(100))
    number = TestNumber(numbers=[1,2,3,4,5])
    with self.assertRaises(ValidationException) as context:
      number.validate(all_fields=False)
    exception = context.exception
    self.assertTrue(len(exception.keypath_messages) == 1)
    self.assertRegex(exception.keypath_messages['numbers.0'], 'Value \'1\' at \'numbers\\.0\' should not be less than 100\\.')

  def test_validate_validates_all_fields_inside_dict(self):
    @jsonclass(graph='test_validate_9')
    class TestNumber(JSONObject):
      numbers: Dict[str, int] = types.dictof(types.int.min(100))
    number = TestNumber(numbers={ 'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5 })
    with self.assertRaises(ValidationException) as context:
      number.validate()
    exception = context.exception
    self.assertTrue(len(exception.keypath_messages) == 5)
    self.assertRegex(exception.keypath_messages['numbers.a'], 'Value \'1\' at \'numbers\\.a\' should not be less than 100\\.')
    self.assertRegex(exception.keypath_messages['numbers.b'], 'Value \'2\' at \'numbers\\.b\' should not be less than 100\\.')
    self.assertRegex(exception.keypath_messages['numbers.c'], 'Value \'3\' at \'numbers\\.c\' should not be less than 100\\.')
    self.assertRegex(exception.keypath_messages['numbers.d'], 'Value \'4\' at \'numbers\\.d\' should not be less than 100\\.')
    self.assertRegex(exception.keypath_messages['numbers.e'], 'Value \'5\' at \'numbers\\.e\' should not be less than 100\\.')

  def test_validate_validates_only_one_field_inside_dict(self):
    @jsonclass(graph='test_validate_10')
    class TestNumber(JSONObject):
      numbers: Dict[str, int] = types.dictof(types.int.min(100))
    number = TestNumber(numbers={ 'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5 })
    with self.assertRaises(ValidationException) as context:
      number.validate(all_fields=False)
    exception = context.exception
    self.assertTrue(len(exception.keypath_messages) == 1)
    self.assertRegex(exception.keypath_messages['numbers.a'], 'Value \'1\' at \'numbers\\.a\' should not be less than 100\\.')

  def test_validate_validates_all_fields_inside_shape(self):
    @jsonclass(graph='test_validate_11')
    class TestNumber(JSONObject):
      numbers: Dict[str, int] = types.shape({
        'a': types.int.min(100),
        'b': types.int.min(100),
        'c': types.int.min(100),
        'd': types.int.min(100),
        'e': types.int.min(100)
      })
    number = TestNumber(numbers={ 'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5 })
    with self.assertRaises(ValidationException) as context:
      number.validate()
    exception = context.exception
    self.assertTrue(len(exception.keypath_messages) == 5)
    self.assertRegex(exception.keypath_messages['numbers.a'], 'Value \'1\' at \'numbers\\.a\' should not be less than 100\\.')
    self.assertRegex(exception.keypath_messages['numbers.b'], 'Value \'2\' at \'numbers\\.b\' should not be less than 100\\.')
    self.assertRegex(exception.keypath_messages['numbers.c'], 'Value \'3\' at \'numbers\\.c\' should not be less than 100\\.')
    self.assertRegex(exception.keypath_messages['numbers.d'], 'Value \'4\' at \'numbers\\.d\' should not be less than 100\\.')
    self.assertRegex(exception.keypath_messages['numbers.e'], 'Value \'5\' at \'numbers\\.e\' should not be less than 100\\.')

  def test_validate_validates_only_one_field_inside_shape(self):
    @jsonclass(graph='test_validate_12')
    class TestNumber(JSONObject):
      numbers: Dict[str, int] = types.shape({
        'a': types.int.min(100),
        'b': types.int.min(100),
        'c': types.int.min(100),
        'd': types.int.min(100),
        'e': types.int.min(100)
      })
    number = TestNumber(numbers={ 'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5 })
    with self.assertRaises(ValidationException) as context:
      number.validate(all_fields=False)
    exception = context.exception
    self.assertTrue(len(exception.keypath_messages) == 1)
    self.assertRegex(exception.keypath_messages['numbers.a'], 'Value \'1\' at \'numbers\\.a\' should not be less than 100\\.')


  def test_validate_validates_all_fields_inside_nested_json_objects(self):
    @jsonclass(graph='test_validate_11')
    class Post(JSONObject):
      title: str = types.str.required
    @jsonclass(graph='test_validate_11')
    class User(JSONObject):
      posts: List[Post] = types.listof(types.instanceof(Post))
    user = User(posts=[{}, {}, {}, {}])
    with self.assertRaises(ValidationException) as context:
      user.validate()
    exception = context.exception
    self.assertTrue(len(exception.keypath_messages) == 4)
    self.assertRegex(exception.keypath_messages['posts.0.title'], 'Value at \'posts\\.0\\.title\' should not be None\\.')
    self.assertRegex(exception.keypath_messages['posts.1.title'], 'Value at \'posts\\.1\\.title\' should not be None\\.')
    self.assertRegex(exception.keypath_messages['posts.2.title'], 'Value at \'posts\\.2\\.title\' should not be None\\.')
    self.assertRegex(exception.keypath_messages['posts.3.title'], 'Value at \'posts\\.3\\.title\' should not be None\\.')

  def test_validate_validates_only_one_field_inside_nested_json_objects(self):
    @jsonclass(graph='test_validate_12')
    class Post(JSONObject):
      title: str = types.str.required
    @jsonclass(graph='test_validate_12')
    class User(JSONObject):
      posts: List[Post] = types.listof(types.instanceof(Post))
    user = User(posts=[{}, {}, {}, {}])
    with self.assertRaises(ValidationException) as context:
      user.validate(all_fields=False)
    exception = context.exception
    self.assertTrue(len(exception.keypath_messages) == 1)
    self.assertRegex(exception.keypath_messages['posts.0.title'], 'Value at \'posts\\.0\\.title\' should not be None\\.')
