from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from tests.classes.any_article import AnyArticle


class TestAny(TestCase):

    def test_any_generates_from_type_hint(self):
        article = AnyArticle(title=True, content=5)
        self.assertEqual(article._data_dict, {'title': True, 'content': 5})

    def test_any_does_not_raise_if_value_is_any_type(self):
        article = AnyArticle(title=True, content=5)
        article.validate()

    def test_any_raises_if_any_type_is_required(self):
        article = AnyArticle(title='True', content=None)
        self.assertRaisesRegex(ValidationException, 'value required', article.validate)
