from __future__ import annotations
from unittest import TestCase
from jsonclasses.exceptions import ValidationException
from tests.classes.email_user import EmailUserAnalysis


class TestEmail(TestCase):

    def test_email_doesnt_raise_if_value_is_valid_email(self):
        analysis = EmailUserAnalysis(username='hello', email='hello@qq.com')
        analysis.validate()

    def test_email_with_underbar_doesnt_raise_if_value_is_valid_email(self):
        analysis = EmailUserAnalysis(username='hello', email='hello_World@qq.com.cn')
        analysis.validate()

    def test_email_with_dot_doesnt_raise_if_email_is_valid_email(self):
        analysis = EmailUserAnalysis(username='hello', email='hello.world@qq.com.cn')
        analysis.validate()

    def test_email_with_single_letter_in_each_field_doesnt_raise_if_email_is_valid_email(self):
        analysis = EmailUserAnalysis(username='hello', email='a@a.a.cn')
        analysis.validate()

    def test_email_with_multiple_domain_doesnt_raise_if_email_is_valid_email(self):
        analysis = EmailUserAnalysis(username='hello', email='a@a.a.cn.a.a')
        analysis.validate()

    def test_email_raises_if_email_is_not_valid_email(self):
        analysis = EmailUserAnalysis(username='hello', email='@qq.com')
        with self.assertRaises(ValidationException) as context:
            analysis.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['email'],
                         "email '@qq.com' at 'email' is not valid email.")

    def test_email_raises_exception_if_email_contain_exclamation_mark(self):
        analysis = EmailUserAnalysis(username='hello', email='!a@qq.com')
        with self.assertRaises(ValidationException) as context:
            analysis.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['email'],
                         "email '!a@qq.com' at 'email' is not valid email.")

    def test_email_raises_exception_if_email_contain_hashtag(self):
        analysis = EmailUserAnalysis(username='hello', email='#@qq.com')
        with self.assertRaises(ValidationException) as context:
            analysis.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['email'],
                         "email '#@qq.com' at 'email' is not valid email.")