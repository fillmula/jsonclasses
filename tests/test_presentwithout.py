from __future__ import annotations
from unittest import TestCase
from jsonclasses.exceptions import ValidationException
from tests.classes.simple_user_account import SimpleUserAccount
from tests.classes.simple_contact import SimpleContact


class TestPresentWithout(TestCase):

    def test_presentwithout_raises_if_both_not_presented(self):
        account = SimpleUserAccount()
        with self.assertRaises(ValidationException) as context:
            account.validate()
        exception = context.exception
        self.assertEqual(len(exception.keypath_messages), 1)
        self.assertEqual(exception.keypath_messages['email'],
                         "Value at 'email' should be present since it's "
                         "referring values are not presented.")

    def test_presentwithout_doesnt_raise_if_one_presented(self):
        SimpleUserAccount(email='a@g.com').validate()
        SimpleUserAccount(phone_number='a@g.com').validate()

    def test_presentwithout_raises_if_non_presented(self):
        contact = SimpleContact()
        with self.assertRaises(ValidationException) as context:
            contact.validate()
        exception = context.exception
        self.assertEqual(len(exception.keypath_messages), 1)
        self.assertEqual(exception.keypath_messages['email'],
                         "Value at 'email' should be present since it's "
                         "referring values are not presented.")

    def test_presentwithout_doesnt_raise_if_one_of_many_presented(self):
        SimpleContact(email='a@g.com').validate()
        SimpleContact(phone_no='a@g.com').validate()
        SimpleContact(address='a@g.com').validate()
