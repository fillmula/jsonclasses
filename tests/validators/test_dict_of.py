import unittest
from typing import Dict
from datetime import datetime, date
from jsonclasses import jsonclass, JSONObject, types
from jsonclasses.exceptions import ValidationException

class TestDictOfValidator(unittest.TestCase):

  def test_list_validator_throws_if_field_value_is_not_list(self):
    @jsonclass(graph='test_dictof_1')
    class Book(JSONObject):
      chapters: Dict[str, str] = types.dict_of(types.str).required
    self.assertRaises(ValidationException, Book(chapters='abc').validate)

  def test_list_validator_throws_if_one_of_item_doesnt_match_inner_validator(self):
    @jsonclass(graph='test_dictof_2')
    class Book(JSONObject):
      chapters: Dict[str, str] = types.dict_of(types.str).required
    book = Book(chapters={ '0': 'abc', '1': 'def', '2': 'ghi', '3': 4, '4': '789' })
    self.assertRaises(ValidationException, book.validate)

  def test_list_validator_does_not_throw_if_all_items_match_inner_validator(self):
    @jsonclass(graph='test_dictof_3')
    class Book(JSONObject):
      chapters: Dict[str, str] = types.dict_of(types.str).required
    book = Book(chapters={ '0': 'abc', '1': 'def', '2': 'ghi', '3': '789' })
    try:
      book.validate()
    except:
      self.fail('list validator should not throw if all items are satisfied.')

  def test_list_validator_accepts_raw_type(self):
    @jsonclass(graph='test_dictof_4')
    class Book(JSONObject):
      chapters: Dict[str, str] = types.dict_of(str).required
    book = Book(chapters={ '0': 'abc', '1': 'def', '2': 'ghi', '3': '789' })
    try:
      book.validate()
    except:
      self.fail('list validator should be ok if raw type passes.')

  def test_list_validator_throws_if_given_values_doesnt_match_raw_type(self):
    @jsonclass(graph='test_dictof_5')
    class Book(JSONObject):
      chapters: Dict[str, str] = types.dict_of(str).required
    book = Book(chapters={ '0': 'abc', '1': 'def', '2': 'ghi', '3': 5 })
    self.assertRaises(ValidationException, book.validate)

  def test_list_validator_transforms_datetime(self):
    @jsonclass(graph='test_dictof_6')
    class Memory(JSONObject):
      days: Dict[str, datetime] = types.dict_of(datetime).required
    memory = Memory(days={ '1': '2020-06-01T02:22:22.222Z', '2': '2020-07-02T02:22:22.222Z' })
    self.assertEqual(memory.days, {
      '1': datetime(2020, 6, 1, 2, 22, 22, 222000),
      '2': datetime(2020, 7, 2, 2, 22, 22, 222000)
    })

  def test_list_validator_transforms_date(self):
    @jsonclass(graph='test_dictof_7')
    class Memory(JSONObject):
      days: Dict[str, date] = types.dict_of(date).required
    memory = Memory(days={ '1': '2020-06-01T00:00:00.000Z', '2': '2020-07-02T00:00:00.000Z' })
    self.assertEqual(memory.days, {
      '1': date(2020, 6, 1),
      '2': date(2020, 7, 2)
    })

  def test_dict_of_convert_datetime_to_json(self):
    @jsonclass(graph='test_dictof_8')
    class Memory(JSONObject):
      days: Dict[str, datetime] = types.dict_of(datetime).required
    memory = Memory(days={ '1': '2020-06-01T02:22:22.222Z', '2': '2020-07-02T02:22:22.222Z' })
    self.assertEqual(memory.tojson(), {
      'days': {
        '1': '2020-06-01T02:22:22.222Z',
        '2': '2020-07-02T02:22:22.222Z'
      }
    })

  def test_dict_of_convert_date_to_json(self):
    @jsonclass(graph='test_dictof_9')
    class Memory(JSONObject):
      days: Dict[str, date] = types.dict_of(date).required
    memory = Memory(days={ '1': '2020-06-01T00:00:00.000Z', '2': '2020-07-02T00:00:00.000Z' })
    self.assertEqual(memory.tojson(), {
     'days': { '1': '2020-06-01T00:00:00.000Z', '2': '2020-07-02T00:00:00.000Z' }
    })

  def test_dict_of_does_not_allow_null_by_default_for_raw_type(self):
    @jsonclass(graph='test_dictof_10')
    class Quiz(JSONObject):
      numbers: Dict[str, int] = types.dict_of(int)
    quiz = Quiz(numbers={ 'a': 0, 'b': 1, 'c': None, 'd': 4, 'e': 5 })
    self.assertRaises(ValidationException, quiz.validate)

  def test_dict_of_does_not_allow_null_by_default_for_typed_type(self):
    @jsonclass(graph='test_dictof_11')
    class Quiz(JSONObject):
      numbers: Dict[str, int] = types.dict_of(types.int)
    quiz = Quiz(numbers={ 'a': 0, 'b': 1, 'c': None, 'd': 4, 'e': 5 })
    self.assertRaises(ValidationException, quiz.validate)

  def test_dict_of_does_allow_null_for_typed_type_marked_with_nullable(self):
    @jsonclass(graph='test_dictof_12')
    class Quiz(JSONObject):
      numbers: Dict[str, int] = types.dict_of(types.int.nullable)
    quiz = Quiz(numbers={ 'a': 0, 'b': 1, 'c': None, 'd': 4, 'e': 5 })
    try:
      quiz.validate()
    except:
      self.fail('nullable marked should allow None in list of validator')

  def test_dict_of_should_camelize_keys_when_serializing_if_its_the_class_setting(self):
    @jsonclass(graph='test_dictof_13')
    class Score(JSONObject):
      scores: Dict[str, int] = types.dict_of(types.int)
      def camelize_json_keys(self) -> bool:
        return True
    score = Score(scores={ 'john_leo': 2, 'peter_sun': 4 })
    self.assertEqual(score.tojson(), { 'scores': { 'johnLeo': 2, 'peterSun': 4 }})

  def test_dict_of_should_not_camelize_keys_when_serializing_if_its_the_class_setting(self):
    @jsonclass(graph='test_dictof_14')
    class Score(JSONObject):
      scores: Dict[str, int] = types.dict_of(types.int)
      def camelize_json_keys(self) -> bool:
        return False
    score = Score(scores={ 'john_leo': 2, 'peter_sun': 4 })
    self.assertEqual(score.tojson(), { 'scores': { 'john_leo': 2, 'peter_sun': 4 }})

  def test_dict_of_should_handle_camelized_keys_when_initializing_if_its_the_class_setting(self):
    @jsonclass(graph='test_dictof_15')
    class Score(JSONObject):
      scores: Dict[str, int] = types.dict_of(types.int)
      def camelize_json_keys(self) -> bool:
        return True
    score = Score(scores={ 'johnLeo': 2, 'peterSun': 4 })
    self.assertEqual(score.__dict__, { 'scores': { 'john_leo': 2, 'peter_sun': 4 }})

  def test_dict_of_should_not_handle_camelized_keys_when_initializing_if_its_the_class_setting(self):
    @jsonclass(graph='test_dictof_16')
    class Score(JSONObject):
      scores: Dict[str, int] = types.dict_of(types.int)
      def camelize_json_keys(self) -> bool:
        return False
    score = Score(scores={ 'johnLeo': 2, 'peterSun': 4 })
    self.assertEqual(score.__dict__, { 'scores': { 'johnLeo': 2, 'peterSun': 4 }})
