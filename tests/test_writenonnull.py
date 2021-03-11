from __future__ import annotations
from unittest import TestCase
from tests.classes.nonnull_user import NonnullUser


class TestWritenonnull(TestCase):

    def test_writenonnull_fields_can_accept_initial_value(self):
        user = NonnullUser(name='Siang Kêk Tsãi Li')
        self.assertEqual(user.name, 'Siang Kêk Tsãi Li')

    def test_writenonnull_fields_can_accept_default_value(self):
        user = NonnullUser()
        self.assertEqual(user.nickname, 'KuiPêkBvang')

    def test_writenonnull_fields_can_accept_nonnull_value(self):
        user = NonnullUser(nickname='Mih Kai')
        user.set(nickname='Si Hao')
        self.assertEqual(user.nickname, 'Si Hao')

    # TODO: make this into exception
    def test_writenonnull_fields_cannot_accept_null_value(self):
        user = NonnullUser(nickname='Khêng Sang')
        user.set(nickname=None)
        self.assertEqual(user.nickname, 'Khêng Sang')
