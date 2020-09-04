import unittest
from typing import List
from datetime import datetime, date
from jsonclasses import jsonclass, JSONObject, types
from jsonclasses.exceptions import ValidationException

class TestListOfValidator(unittest.TestCase):

  def test_list_validator_throws_if_field_value_is_not_list(self):
    @jsonclass
    class Book(JSONObject):
      chapters: List[str] = types.list_of(types.str).required
    self.assertRaises(ValidationException, Book(chapters='abc').validate)

  def test_list_validator_throws_if_one_of_item_doesnt_match_inner_validator(self):
    @jsonclass
    class Book(JSONObject):
      chapters: List[str] = types.list_of(types.str).required
    book = Book(chapters=['abc', 'def', 'ghi', 4, '789'])
    self.assertRaises(ValidationException, book.validate)

  def test_list_validator_does_not_throw_if_all_items_match_inner_validator(self):
    @jsonclass
    class Book(JSONObject):
      chapters: List[str] = types.list_of(types.str).required
    book = Book(chapters=['abc', 'def', 'ghi', '789'])
    try:
      book.validate()
    except:
      self.fail('list validator should not throw if all items are satisfied.')

  def test_list_validator_accepts_raw_type(self):
    @jsonclass
    class Book(JSONObject):
      chapters: List[str] = types.list_of(str).required
    book = Book(chapters=['abc', 'def', 'ghi', '789'])
    try:
      book.validate()
    except:
      self.fail('list validator should be ok if raw type passes.')

  def test_list_validator_throws_if_given_values_doesnt_match_raw_type(self):
    @jsonclass
    class Book(JSONObject):
      chapters: List[str] = types.list_of(str).required
    book = Book(chapters=['abc', 'def', 'ghi', 5])
    self.assertRaises(ValidationException, book.validate)

  def test_list_validator_transforms_datetime(self):
    @jsonclass
    class Memory(JSONObject):
      days: List[datetime] = types.list_of(datetime).required
    memory = Memory(days=['2020-06-01T02:22:22.222Z', '2020-07-02T02:22:22.222Z'])
    self.assertEqual(memory.days, [
      datetime(2020, 6, 1, 2, 22, 22, 222000),
      datetime(2020, 7, 2, 2, 22, 22, 222000)
    ])

  def test_list_validator_transforms_date(self):
    @jsonclass
    class Memory(JSONObject):
      days: List[date] = types.list_of(date).required
    memory = Memory(days=['2020-06-01T00:00:00.000Z', '2020-07-02T00:00:00.000Z'])
    self.assertEqual(memory.days, [
      date(2020, 6, 1),
      date(2020, 7, 2)
    ])

  def test_list_of_convert_datetime_to_json(self):
    @jsonclass
    class Memory(JSONObject):
      days: List[datetime] = types.list_of(datetime).required
    memory = Memory(days=['2020-06-01T02:22:22.222Z', '2020-07-02T02:22:22.222Z'])
    self.assertEqual(memory.tojson(), {
      'days': ['2020-06-01T02:22:22.222Z', '2020-07-02T02:22:22.222Z']
    })

  def test_list_of_convert_date_to_json(self):
    @jsonclass
    class Memory(JSONObject):
      days: List[date] = types.list_of(date).required
    memory = Memory(days=['2020-06-01T00:00:00.000Z', '2020-07-02T00:00:00.000Z'])
    self.assertEqual(memory.tojson(), {
      'days': ['2020-06-01T00:00:00.000Z', '2020-07-02T00:00:00.000Z']
    })
