from __future__ import annotations
from unittest import TestCase
from jsonclasses.exceptions import ValidationException
from tests.classes.simple_auth_code import SimpleAuthCode


class TestPresentWith(TestCase):

    def test_presentwith_raises_if_refering_present_value_not_present(self):
        code = SimpleAuthCode(phone_number='+8613012345678', code='4466')
        with self.assertRaises(ValidationException) as context:
            code.validate()
        exception = context.exception
        self.assertEqual(len(exception.keypath_messages), 1)
        self.assertEqual(exception.keypath_messages['calling_code'],
                         "Value at 'calling_code' should be present since "
                         "it's referring value is presented.")

    def test_presentwith_doesnt_raise_if_both_value_not_present(self):
        code = SimpleAuthCode(code='4466')
        code.validate()

    def test_presentwith_doesnt_raise_if_both_value_present(self):
        code = SimpleAuthCode(code='4466',
                              phone_number='+86123',
                              calling_code='+86123')
        code.validate()

    def test_presentwith_doesnt_raise_if_refering_not_present(self):
        code = SimpleAuthCode(code='4466', calling_code='+86123')
        code.validate()
