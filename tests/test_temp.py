from __future__ import annotations
from unittest import TestCase
from jsonclasses.exceptions import ValidationException
from tests.classes.simple_authcode import SimpleAuthcode


class TestTemp(TestCase):

    def test_temp_value_does_not_go_to_json(self):
        code = SimpleAuthcode(name='code', code='1234')
        self.assertEqual(code.tojson(), {'name': 'code'})

    def test_temp_fields_are_cleared_after_write(self):
        code = SimpleAuthcode(name='code', code='1234')
        code._clear_temp_fields()
        self.assertEqual(code.code, None)

    def test_temp_fields_are_validated(self):
        code = SimpleAuthcode(name='code')
        with self.assertRaises(ValidationException):
            code.validate()
