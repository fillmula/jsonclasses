from unittest import TestCase
from tests.classes.simple_article import SimpleArticle


class TestJSONClass(TestCase):

    def test_initialize_without_arguments(self):
        article = SimpleArticle()
        self.assertEqual(article._data_dict, {'title': None, 'content': None})
