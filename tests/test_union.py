from __future__ import annotations
from datetime import datetime
from unittest import TestCase
from jsonclasses.excs import ValidationException
from tests.classes.simple_mixed import SimpleMixed, SimpleMixedT, SimpleMixedU


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

    def test_union_transform_use_matched_transform(self):
        one = SimpleMixedT(value=50)
        self.assertEqual(one.value, 173)
        two = SimpleMixedT(value='50')
        self.assertEqual(two.value, '50123')

    def test_union_tojson_use_matched_displayer(self):
        one = SimpleMixedU(value='2021-10-16T13:43:28.099Z')
        self.assertEqual(one.value, datetime(2021, 10, 16, 13, 43, 28, 99000))
        two = SimpleMixedU(value='123')
        self.assertEqual(two.value, '123')
        self.assertEqual(one.tojson()['value'], '2021-10-16T13:43:28.099Z')
        self.assertEqual(two.tojson()['value'], '123')
