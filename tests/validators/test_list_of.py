import unittest
from typing import List
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
    book.validate()
