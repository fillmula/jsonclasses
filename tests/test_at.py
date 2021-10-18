from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from tests.classes.simple_at import SimpleAt


class TestAt(TestCase):
    def test_at_gets_the_index_value_of_original_value(self):
        obj = SimpleAt(a={"name": "ben", "sex": "male"})
        self.assertEqual(obj.a, "ben")

    def test_at_gets_the_index_value_of_original_value_with_callable(self):
        obj = SimpleAt(ca={"name": "ben", "sex": "male"})
        self.assertEqual(obj.ca, "ben")

    def test_at_gets_the_index_value_of_original_value_with_types(self):
        obj = SimpleAt(ta={"name": "ben", "sex": "male"})
        self.assertEqual(obj.ta, "ben")
