from __future__ import annotations
from unittest import TestCase
from tests.classes.cb_book import CBBook
from tests.classes.cbm_book import CBMBook
from tests.classes.cbo_book import CBOBook


class TestDecoratedOnSave(TestCase):

    def test_callback_are_not_called_for_new_objects_on_save(self):
        book = CBBook(name='N', content='C')
        book.save()
        self.assertEqual(book.updated_count, 0)

    def test_callback_are_called_for_existing_objects_on_save(self):
        book = CBBook(name='N', content='C')
        setattr(book, '_is_new', False)
        book.save()
        self.assertEqual(book.updated_count, 1)

    def test_multiple_callbacks_are_not_called_for_new_objects_on_save(self):
        book = CBMBook(name='N', content='C')
        book.save()
        self.assertEqual(book.updated_count, 0)

    def test_multiple_callbacks_are_called_for_existing_objects_on_save(self):
        book = CBMBook(name='N', content='C')
        setattr(book, '_is_new', False)
        book.save()
        self.assertEqual(book.updated_count, 2)

    def test_operator_can_be_passed_into_callback(self):
        book = CBOBook(name='N', content='C')
        setattr(book, '_is_new', False)
        book.opby(10)
        book.save()
        self.assertEqual(book.updated_count, 10)
