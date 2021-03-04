from unittest import TestCase
from tests.classes.simple_article import SimpleArticle
from tests.classes.simple_order import SimpleOrder


class TestInitialize(TestCase):

    def test_initialize_simple_object_without_arguments(self):
        article = SimpleArticle()
        self.assertEqual(article._data_dict, {'title': None, 'content': None})

    def test_initialize_simple_object_with_arguments(self):
        article = SimpleArticle(title='Oi', content='Tik')
        self.assertEqual(article._data_dict, {'title': 'Oi', 'content': 'Tik'})

    def test_initialize_simple_object_with_default_values(self):
        order = SimpleOrder(name='Oi Tik')
        self.assertEqual(order._data_dict, {'name': 'Oi Tik', 'quantity': 1})
