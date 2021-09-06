from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from tests.classes.simple_mixed import SimpleMixed


class TestUnion(TestCase):

    def test_union_raises_if_none_matches(self):
        mixed = SimpleMixed(name='Mixed', mixed=5.0)
        with self.assertRaises(ValidationException):
            mixed.validate()

    def test_union_does_not_raise_if_any_matches(self):
        mixed = SimpleMixed(name='Mixed', mixed=5)
        mixed.validate()
        mixed1 = SimpleMixed(name='Mixed', mixed='5')
        mixed1.validate()
