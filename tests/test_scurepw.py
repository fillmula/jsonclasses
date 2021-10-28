from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from tests.classes.super_str import SuperStr


class TestSecurepw(TestCase):

    def test_securepw_does_not_raise_if_value_is_scure_password(self):
        pw = SuperStr(securepw='w4Hsa/')
        pw.validate()

    def test_securepw_raises_if_value_is_not_scure_password(self):
        pw = SuperStr(securepw='w4Hsa')
        with self.assertRaises(ValidationException) as context:
             pw.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['securepw'],
                         "value is not secure password")
