from __future__ import annotations
from unittest import TestCase
from jsonclasses.exceptions import ValidationException
from tests.classes.linked_author import LinkedAuthor
from tests.classes.linked_article import LinkedArticle


class TestLocalKey(TestCase):

    def test_local_key_can_be_accessed(self):
        article = LinkedArticle(name='A')
        self.assertEqual(article.author_id, None)
