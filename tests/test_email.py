from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from tests.classes.email_user import EmailUser


class TestEmail(TestCase):

    def test_simple_email_doesnt_raise(self):
        analysis = EmailUser(username='hello', email='hello@qq.com')
        analysis.validate()

    def test_email_with_underbar_doesnt_raise(self):
        analysis = EmailUser(username='hello', email='hello_World@qq.com.cn')
        analysis.validate()

    def test_email_with_dot_doesnt_raise(self):
        analysis = EmailUser(username='hello', email='hello.world@qq.com.cn')
        analysis.validate()

    def test_email_with_single_letter_in_each_field_doesnt_raise(self):
        analysis = EmailUser(username='hello', email='a@a.a.cn')
        analysis.validate()

    def test_email_with_multiple_domains_doesnt_raise(self):
        analysis = EmailUser(username='hello', email='a@a.a.cn.a.a')
        analysis.validate()

    def test_email_raises_if_value_is_not_valid_email(self):
        analysis = EmailUser(username='hello', email='@qq.com')
        with self.assertRaises(ValidationException) as context:
            analysis.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['email'],
                         "value is not email string")

    def test_email_raises_if_email_contains_special_charaters(self):
        analysis = EmailUser(username='hello', email='!a@qq.com')
        with self.assertRaises(ValidationException) as context:
            analysis.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['email'],
                         "value is not email string")

    def test_email_raises_exception_if_email_contains_hashtag(self):
        analysis = EmailUser(username='hello', email='#@qq.com')
        with self.assertRaises(ValidationException) as context:
            analysis.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['email'],
                         "value is not email string")
