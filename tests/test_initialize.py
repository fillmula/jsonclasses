from __future__ import annotations
from unittest import TestCase
from jsonclasses.exceptions import ValidationException
from tests.classes.simple_article import SimpleArticle
from tests.classes.simple_order import SimpleOrder
from tests.classes.simple_address import SimpleAddress


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

    def test_initialize_do_not_accept_undefined_keys_by_default(self):
        with self.assertRaises(ValidationException) as context:
            SimpleArticle(dzimsikai='Ku Piang Hoê')
        self.assertTrue(len(context.exception.keypath_messages) == 1)
        self.assertEqual(context.exception.keypath_messages['dzimsikai'],
                         "Key 'dzimsikai' is not allowed.")

    def test_initialize_underscore_key_cases_by_default(self):
        address = SimpleAddress(**{'lineOne': 'NgouOu', 'lineTwo': 'Sihai'})
        self.assertEqual(address._data_dict,
                         {'line_one': 'NgouOu', 'line_two': 'Sihai'})
