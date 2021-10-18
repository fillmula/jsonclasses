from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from tests.classes.simple_range import SimpleRange

class TestRange(TestCase):

    def test_range_does_not_raise_if_value_is_in_range(self):
        i = SimpleRange(i=5)
        i.validate()

    def test_range_does_not_raise_if_value_is_in_callable_range(self):
        i = SimpleRange(ic=5)
        i.validate()

    def test_range_does_not_raise_if_value_is_in_types_range(self):
        i = SimpleRange(it=5)
        i.validate()

    def test_range_raises_if_value_is_not_in_range(self):
        i = SimpleRange(i=11)
        with self.assertRaises(ValidationException) as context:
            i.validate()
        self.assertEqual(context.exception.keypath_messages['i'],
                         "value is not less than or equal 10")
