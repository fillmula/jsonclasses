from __future__ import annotations
from unittest import TestCase
from jsonclasses.exceptions import UnauthorizedActionException
from tests.classes.gs_article import GSArticle, GSAuthor
from tests.classes.gm_article import GMArticle, GMAuthor


class TestCanCreate(TestCase):

    def test_guards_raises_if_no_operator_is_assigned(self):
        article = GSArticle(name='P', content='C')
        paid_author = GSAuthor(id='P', name='A', paid_user=True)
        article.author = paid_author
        with self.assertRaises(UnauthorizedActionException):
            article.save()

    def test_guards_are_called_for_new_objects_on_save(self):
        article = GSArticle(name='P', content='C')
        paid_author = GSAuthor(id='P', name='A', paid_user=True)
        article.author = paid_author
        article.opby(paid_author)
        article.save()
        free_author = GSAuthor(id='F', name='A', paid_user=False)
        article.author = free_author
        article.opby(free_author)
        with self.assertRaises(UnauthorizedActionException):
            article.save()

    def test_guards_are_not_called_for_existing_objects_on_save(self):
        article = GSArticle(name='P', content='C')
        setattr(article, '_is_new', False)
        paid_author = GSAuthor(id='P', name='A', paid_user=True)
        article.author = paid_author
        article.opby(paid_author)
        article.save()
        free_author = GSAuthor(id='F', name='A', paid_user=False)
        article.author = free_author
        article.opby(free_author)
        article.save()

    def test_multiple_guards_are_called_for_new_objects_on_save(self):
        article = GMArticle(name='P', content='C')
        paid_author = GMAuthor(id='P', name='A', paid_user=True)
        article.author = paid_author
        article.opby(paid_author)
        article.save()
        free_author = GMAuthor(id='F', name='A', paid_user=False)
        article.author = free_author
        article.opby(free_author)
        with self.assertRaises(UnauthorizedActionException):
            article.save()

    def test_multiple_guards_are_not_called_for_existing_objects_on_save(self):
        article = GMArticle(name='P', content='C')
        setattr(article, '_is_new', False)
        paid_author = GMAuthor(id='P', name='A', paid_user=True)
        article.author = paid_author
        article.opby(paid_author)
        article.save()
        free_author = GMAuthor(id='F', name='A', paid_user=False)
        article.author = free_author
        article.opby(free_author)
        article.save()
