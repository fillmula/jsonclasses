from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from tests.classes.simple_match import SimpleMatch

class TestMatch(TestCase):

    def test_match_does_not_raise_if_matched(self):
        s = SimpleMatch(m="asdsd")
        s.validate()

    def test_match_does_not_raise_if_matched_with_callable_match_str(self):
        s = SimpleMatch(cm="asdsd")
        s.validate()

    def test_match_does_not_raise_if_matched_with_types_match_str(self):
        s = SimpleMatch(tm="asdsd")
        s.validate()

    def test_match_raise_if_it_is_not_matched(self):
        s = SimpleMatch(m="ffsdsd")
        with self.assertRaises(ValidationException) as context:
            s.validate()
        self.assertEqual(context.exception.keypath_messages['m'],
                         "value does not match '^a.*'")
