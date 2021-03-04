from __future__ import annotations
from unittest import TestCase
from jsonclasses.exceptions import ValidationException
from tests.classes.simple_book import SimpleBook


class TestBool(TestCase):

    def test_bool_is_bool_after_assigned(self):
        book = SimpleBook(published=True)
        self.assertEqual(book._data_dict, {'name': None, 'published': True})

    def test_bool_raises_if_value_is_not_bool(self):
        book = SimpleBook(published=1)
        with self.assertRaises(ValidationException) as context:
            book.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['published'],
                         "Value '1' at 'published' should be bool.")

    def test_bool_is_bool_when_tojson(self):
        book = SimpleBook(published=False)
        self.assertEqual(book.tojson(), {'name': None, 'published': False})
