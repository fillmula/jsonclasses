from __future__ import annotations
from unittest import TestCase
from jsonclasses.exceptions import ValidationException
from tests.classes.simple_article import SimpleArticle
from tests.classes.simple_tenant import SimpleTenant
from tests.classes.author import Author


class TestStrict(TestCase):

    def test_strict_raises_in_init_on_unallowed_keys(self):
        with self.assertRaises(ValidationException) as context:
            SimpleArticle(author='Victor Teo')
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['author'],
                         "Key 'author' is not allowed.")

    def test_without_strict_nothing_raises_in_init_on_unallowed_keys(self):
        tenant = SimpleTenant(name='Victor Teo', host='Emily Ho')
        self.assertEqual(tenant._data_dict,
                         {'name': 'Victor Teo', 'age': None})

    def test_strict_raises_in_set_on_unallowed_keys(self):
        article = SimpleArticle(title='Tshio Ue', content='Mai Tshio')
        with self.assertRaises(ValidationException) as context:
            article.set(author='Victor Teo')
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['author'],
                         "Key 'author' is not allowed.")

    def test_without_strict_nothing_raises_in_set_on_unallowed_keys(self):
        tenant = SimpleTenant(name='Victor Teo', host='Emily Ho')
        tenant.set(age=30, id='abcdefghi')
        self.assertEqual(tenant._data_dict,
                         {'name': 'Victor Teo', 'age': 30})

    def test_update_always_raises_on_unallowed_keys_regardless_of_strict(self):
        tenant = SimpleTenant(name='Victor Teo', age=30)
        with self.assertRaises(ValueError):
            tenant.update(host='Emily')

    def test_strict_uses_object_config_in_nested_init(self):
        author = Author(name='Nge', articles=[
            {'title': 'A1', 'content': 'C1', 'published': True},
            {'title': 'A2', 'content': 'C2', 'published': True}])
        self.assertEqual(author.articles[0]._data_dict,
                         {'title': 'A1', 'content': 'C1', 'author': author})
        self.assertEqual(author.articles[1]._data_dict,
                         {'title': 'A2', 'content': 'C2', 'author': author})
