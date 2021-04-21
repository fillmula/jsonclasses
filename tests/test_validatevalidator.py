from __future__ import annotations
from unittest import TestCase
from jsonclasses.exceptions import ValidationException
from tests.classes.valid_password import (ValidPassword, ValidPasswordMessage,
                                          CValidPassword, OptionalPassword)


class TestValidateValidator(TestCase):

    def test_validate_wont_validate_none(self):
        opw = OptionalPassword(name='Bo Lang', password=None)
        opw.validate()

    def test_validate_is_fine_when_validator_returns_true(self):
        pw = ValidPassword(name='Li Si', password='0000')
        try:
            pw.validate()
        except ValidationException:
            self.fail('validate should be fine if value is valid')

    def test_validate_raises_default_msg_when_validator_returns_false(self):
        pw = ValidPassword(name='Li Si', password='000')
        self.assertRaisesRegex(ValidationException,
                               'invalid value',
                               pw.validate)

    def test_validate_raises_if_validator_returns_str(self):
        pw = ValidPasswordMessage(name='Li Si', password='000')
        self.assertRaisesRegex(ValidationException, 'wrong', pw.validate)

    def test_validate_is_fine_when_validator_returns_none(self):
        pw = ValidPasswordMessage(name='Li Si', password='0000')
        pw.validate()

    def test_validate_can_also_accept_context(self):
        pw = CValidPassword(name='Li Si', password='0000')
        pw.validate()
