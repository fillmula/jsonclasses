from __future__ import annotations
from unittest import TestCase
from tests.classes.simple_secret import SimpleSecret


class TestInternal(TestCase):

    def test_internal_cannot_be_set_through_init(self):
        secret = SimpleSecret(name='1', message='2')
        self.assertEqual(secret._data_dict, {'name': '1', 'message': None})

    def test_internal_cannot_be_set_through_set(self):
        secret = SimpleSecret(name='1', message='2')
        secret.set(message='4')
        self.assertEqual(secret._data_dict, {'name': '1', 'message': None})

    def test_internal_can_be_set_through_update(self):
        secret = SimpleSecret(name='1', message='2')
        secret.update(message='4')
        self.assertEqual(secret._data_dict, {'name': '1', 'message': '4'})

    def test_internal_can_be_set_through_assign(self):
        secret = SimpleSecret(name='1', message='2')
        secret.message = '5'
        self.assertEqual(secret._data_dict, {'name': '1', 'message': '5'})

    def test_internal_wont_appear_in_output(self):
        secret = SimpleSecret(name='1', message='2')
        secret.message = '5'
        self.assertEqual(secret.tojson(), {'name': '1'})
