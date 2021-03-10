from __future__ import annotations
from unittest import TestCase
from tests.classes.simple_secret import SimpleSecret


class TestTrim(TestCase):

    def test_trim_trims_str(self):
        secret = SimpleSecret(name='  1  ', message='2')
        self.assertEqual(secret.name, '1')
