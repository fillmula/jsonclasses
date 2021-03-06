from __future__ import annotations
from unittest import TestCase
from jsonclasses.exceptions import ValidationException
from tests.classes.simple_article import SimpleArticle
from tests.classes.simple_tenant import SimpleTenant


class TestStrict(TestCase):

    def test_strict_raises_in_init_on_unallowed_keys(self):
        with self.assertRaises(ValidationException) as context:
            SimpleArticle(authur='Victor Teo')
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['authur'],
                         "Key 'authur' is not allowed.")

    def test_without_strict_nothing_raises_in_init_on_unallowed_keys(self):
        tenant = SimpleTenant(name='Victor Teo', host='Emily Ho')
        self.assertEqual(tenant._data_dict,
                         {'name': 'Victor Teo', 'age': None})

    def test_strict_raises_in_set_on_unallowed_keys(self):
        article = SimpleArticle(title='Tshio Ue', content='Mai Tshio')
        with self.assertRaises(ValidationException) as context:
            article.set(authur='Victor Teo')
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['authur'],
                         "Key 'authur' is not allowed.")

    def test_without_strict_nothing_raises_in_set_on_unallowed_keys(self):
        tenant = SimpleTenant(name='Victor Teo', host='Emily Ho')
        tenant.set(age=30, id='abcdefghi')
        self.assertEqual(tenant._data_dict,
                         {'name': 'Victor Teo', 'age': 30})

    def test_update_always_raises_on_unallowed_keys_regardless_of_strict(self):
        tenant = SimpleTenant(name='Victor Teo', age=30)
        with self.assertRaises(ValueError):
            tenant.update(host='Emily')
