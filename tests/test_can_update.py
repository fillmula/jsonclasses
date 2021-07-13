from __future__ import annotations
from unittest import TestCase
from jsonclasses.exceptions import UnauthorizedActionException
from tests.classes.gs_book import GSBookAuthor, GSBook
from tests.classes.gm_book import GMBookAuthor, GMBook


class TestCanUpdate(TestCase):

    def test_guards_raises_if_no_operator_is_assigned(self):
        book = GSBook(name='P')
        setattr(book, '_is_new', False)
        paid_author = GSBookAuthor(id='P', name='A', paid_user=True)
        book.author = paid_author
        with self.assertRaises(UnauthorizedActionException):
            book.save()

    def test_guards_are_not_called_for_new_objects_on_save(self):
        book = GSBook(name='P')
        paid_author = GSBookAuthor(id='P', name='A', paid_user=True)
        book.author = paid_author
        book.opby(paid_author)
        book.save()
        free_author = GSBookAuthor(id='F', name='A', paid_user=False)
        book.author = free_author
        book.opby(free_author)
        book.save()

    def test_guards_are_called_for_existing_objects_on_save(self):
        book = GSBook(name='P')
        setattr(book, '_is_new', False)
        paid_author = GSBookAuthor(id='P', name='A', paid_user=True)
        book.author = paid_author
        book.opby(paid_author)
        book.save()
        free_author = GSBookAuthor(id='F', name='A', paid_user=False)
        book.author = free_author
        book.opby(free_author)
        with self.assertRaises(UnauthorizedActionException):
            book.save()

    def test_multiple_guards_are_not_called_for_new_objects_on_save(self):
        book = GMBook(name='P')
        paid_author = GMBookAuthor(id='P', name='A', paid_user=True)
        book.author = paid_author
        book.opby(paid_author)
        book.save()
        free_author = GMBookAuthor(id='F', name='A', paid_user=False)
        book.author = free_author
        book.opby(free_author)
        book.save()

    def test_multiple_guards_are_called_for_existing_objects_on_save(self):
        book = GMBook(name='P')
        setattr(book, '_is_new', False)
        paid_author = GMBookAuthor(id='P', name='A', paid_user=True)
        book.author = paid_author
        book.opby(paid_author)
        book.save()
        free_author = GMBookAuthor(id='F', name='A', paid_user=False)
        book.author = free_author
        book.opby(free_author)
        with self.assertRaises(UnauthorizedActionException):
            book.save()
