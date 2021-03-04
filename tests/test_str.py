from __future__ import annotations
from unittest import TestCase
from jsonclasses.exceptions import ValidationException
from tests.classes.simple_article import SimpleArticle


class TestStr(TestCase):

    def test_str_is_str_after_assigned(self):
        article = SimpleArticle(title='Lak Lak')
        self.assertEqual(article._data_dict,
                         {'title': 'Lak Lak', 'content': None})

    def test_str_raises_if_value_is_not_string(self):
        article = SimpleArticle(title=66)
        with self.assertRaises(ValidationException) as context:
            article.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['title'],
                         "Value '66' at 'title' should be str.")

    def test_str_is_str_when_tojson(self):
        article = SimpleArticle(title='Lak Lak')
        self.assertEqual(article.tojson(),
                         {'title': 'Lak Lak', 'content': None})
