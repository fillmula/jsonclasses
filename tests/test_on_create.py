from __future__ import annotations
from unittest import TestCase
from tests.classes.cb_article import CBArticle
from tests.classes.cbm_article import CBMArticle
from tests.classes.cbo_article import CBOArticle


class TestDecoratedOnCreate(TestCase):

    def test_callback_are_called_for_new_objects_on_save(self):
        article = CBArticle(name='A', content='B')
        article.save()
        self.assertEqual(len(article.revisions), 1)
        self.assertEqual(article.revisions[0].name, 'First')

    def test_callback_are_not_called_for_existing_objects_on_save(self):
        article = CBArticle(name='A', content='B')
        setattr(article, '_is_new', False)
        article.save()
        self.assertEqual(len(article.revisions), 0)

    def test_multiple_callbacks_are_called_for_new_objects_on_save(self):
        article = CBMArticle(name='A', content='B')
        article.save()
        self.assertEqual(len(article.revisions), 1)
        self.assertEqual(article.revisions[0].name, 'First')
        self.assertEqual(article.content, 'UPDATED')

    def test_multiple_callbacks_are_not_called_for_existing_objects_on_save(self):
        article = CBMArticle(name='A', content='B')
        setattr(article, '_is_new', False)
        article.save()
        self.assertEqual(len(article.revisions), 0)
        self.assertEqual(article.content, 'B')

    def test_operator_can_be_passed_into_callback(self):
        article = CBOArticle(name='A', content='B')
        article.opby('operator 1')
        article.save()
        self.assertEqual(len(article.revisions), 1)
        self.assertEqual(article.revisions[0].name, 'operator 1')
        self.assertEqual(article.content, 'operator 1')
