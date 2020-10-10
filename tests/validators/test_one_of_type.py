import unittest
from typing import Union
from datetime import datetime, date
from jsonclasses import jsonclass, JSONObject, types
from jsonclasses.exceptions import ValidationException


class TestOneOfTypeValidator(unittest.TestCase):

    def test_one_of_type_should_raise_if_none_match(self):
        @jsonclass(class_graph='test_one_of_type_1')
        class Book(JSONObject):
            val: Union[str, int] = types.oneoftype([str, int]).required
        book = Book(val=True)
        self.assertRaises(ValidationException, book.validate)

    def test_one_of_type_should_not_raise_if_match(self):
        @jsonclass(class_graph='test_one_of_type_2')
        class Book(JSONObject):
            val: Union[str, int] = types.oneoftype([str, int]).required
        book = Book(val=5)
        book2 = Book(val="qbc")
        book.validate()
        book2.validate()
