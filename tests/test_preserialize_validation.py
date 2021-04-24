from unittest import TestCase
from jsonclasses.exceptions import ValidationException
from tests.classes.ps_user import (PsUserL, PsUserN, PsUserV, PsUserD, PsUserT,
                                   PsUserE, PsUserE2, PsUserE3, PsUserCV,
                                   PsUserLE, PsUserDI, PsUserDE, PsUserS,
                                   PsUserSE)


class TestPreserializeValidator(TestCase):

    def test_preserialize_validator_validates_on_save(self):
        with self.assertRaises(ValidationException) as context:
            user = PsUserN(username='123')
            user._set_on_save()
        exception = context.exception
        self.assertEqual(exception.keypath_messages['updated_at'], "Value at 'updated_at' should not be None.")

    def test_preserialize_validator_does_not_validate_on_normal_validate(self):
        user = PsUserN(username='123')
        user.validate()

    def test_preserialize_validator_does_not_raise_if_valid_on_save(self):
        user = PsUserV(username='123')
        user._set_on_save()

    def test_preserialize_validator_setonsave_is_chained_2(self):
        user = PsUserD(username='123')
        user._set_on_save()
        self.assertEqual(user.updated_at, 4)

    def test_preserialize_validator_setonsave_is_chained_3(self):
        user = PsUserT(username='123')
        user._set_on_save()
        self.assertEqual(user.updated_at, 5)

    def test_preserialize_validator_validate_between_chains(self):
        with self.assertRaises(ValidationException) as context:
            user = PsUserE(username='123')
            user._set_on_save()
        exception = context.exception
        self.assertEqual(exception.keypath_messages['updated_at'], "wrong")

    def test_preserialize_validator_validate_between_chains_2(self):
        with self.assertRaises(ValidationException) as context:
            user = PsUserE2(username='123')
            user._set_on_save()
        exception = context.exception
        self.assertEqual(exception.keypath_messages['updated_at'], "wrong")

    def test_preserialize_validator_validate_after_chains(self):
        with self.assertRaises(ValidationException) as context:
            user = PsUserE3(username='123')
            user._set_on_save()
        exception = context.exception
        self.assertEqual(exception.keypath_messages['updated_at'], "wrong")

    def test_preserialize_validator_validate_between_chains_do_not_throw_if_valid(self):
        user = PsUserCV(username='123')
        user._set_on_save()

    def test_preserialize_validator_should_validate_and_setonsave_inside_list(self):
        user = PsUserL(counts=[123, 456])
        user._set_on_save()
        self.assertEqual(user.counts[0], 124)
        self.assertEqual(user.counts[1], 457)

    def test_preserialize_validator_should_validate_and_throw_inside_list(self):
        with self.assertRaises(ValidationException) as context:
            user = PsUserLE(counts=[123, 456])
            user._set_on_save()
        exception = context.exception
        self.assertEqual(exception.keypath_messages['counts.0'], "Value at 'counts.0' should not be None.")

    def test_preserialize_validator_should_validate_and_setonsave_inside_dict(self):
        user = PsUserDI(counts={'a': 123, 'b': 456})
        user._set_on_save()
        self.assertEqual(user.counts['a'], 124)
        self.assertEqual(user.counts['b'], 457)

    def test_preserialize_validator_should_validate_and_throw_inside_dict(self):
        with self.assertRaises(ValidationException) as context:
            user = PsUserDE(counts={'a': 123, 'b': 456})
            user._set_on_save()
        exception = context.exception
        self.assertEqual(exception.keypath_messages['counts.a'], "Value at 'counts.a' should not be None.")

    def test_preserialize_validator_should_validate_and_setonsave_inside_shape(self):
        user = PsUserS(counts={'a': 123, 'b': 456})
        user._set_on_save()
        self.assertEqual(user.counts['a'], 124)
        self.assertEqual(user.counts['b'], 457)

    def test_preserialize_validator_should_validate_and_throw_inside_shape(self):
        with self.assertRaises(ValidationException) as context:
            user = PsUserSE(counts={'a': 123, 'b': 456})
            user._set_on_save()
        exception = context.exception
        self.assertEqual(exception.keypath_messages['counts.b'], "Value at 'counts.b' should not be None.")
