from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from tests.classes.super_message import SuperMessage


class TestVMsgModifier(TestCase):

    def test_vmsg_outputs_custom_error_message_on_invalid(self):
        message = SuperMessage(name='123')
        with self.assertRaises(ValidationException) as context:
            message.validate()
        self.assertEqual(context.exception.keypath_messages, {
            'name': 'MUST 666'
        })

    def test_vmsg_does_not_output_custom_error_message_on_valid(self):
        message = SuperMessage(name='123456')
        message.validate()
