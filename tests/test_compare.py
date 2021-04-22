from __future__ import annotations
from unittest import TestCase
from typing import Optional
from jsonclasses import jsonclass, types
from jsonclasses.exceptions import ValidationException
from jsonclasses.contexts import ValidatingContext
from tests.classes.compare_user import (CompareUser, CompareUserB,
                                        CompareUserS, check_value, check_args)


class TestCompare(TestCase):

    def test_compare_will_not_trigger_for_new_objects(self):
        val = check_value()
        user = CompareUser(age=65)
        user.validate()
        self.assertEqual(val, check_value())

    def test_compare_is_called_once_on_validate_if_field_is_modified(self):
        val = check_value()
        user = CompareUser(age=65)
        setattr(user, '_is_new', False)
        user.age = 60
        user.validate()
        self.assertEqual(val + 1, check_value())
        self.assertEqual(check_args(), (65, 60))

    def test_compare_is_not_called_on_validate_if_field_is_not_modified(self):
        val = check_value()
        user = CompareUser(age=65, name='Pieng Iu')
        setattr(user, '_is_new', False)
        user.name = 'Tao Tin Lai Puah'
        user.validate()
        self.assertEqual(val, check_value())

    def test_compare_is_valid_if_callback_returns_true(self):
        user = CompareUserB(age=65, name='Pieng Iu')
        setattr(user, '_is_new', False)
        user.age = 66
        user.validate()

    def test_compare_is_invalid_if_callback_returns_false(self):
        user = CompareUserB(age=65, name='Pieng Iu')
        setattr(user, '_is_new', False)
        user.age = 70
        self.assertRaisesRegex(ValidationException,
                               'compare failed',
                               user.validate)

    def test_compare_is_invalid_if_str_is_returned(self):
        user = CompareUserS(age=65)
        setattr(user, '_is_new', False)
        user.age = 70
        self.assertRaisesRegex(ValidationException,
                               'invalid',
                               user.validate)

    def test_compare_accepts_ctx(self):
        user = CompareUserS(age=0)
        setattr(user, '_is_new', False)
        user.age = 50
        user.validate()

    # def test_compare_takes_ctx(self):

    #     val = {'val': '123'}

    #     def compare(old: int, new: int, key_path: str, obj: User, ctx: ValidatingContext):
    #         val['val'] = ctx

    #     @jsonclass(class_graph='test_compare_9')
    #     class User:
    #         age: Optional[int] = types.int.compare(compare).required
    #     user = User(age=1)
    #     setattr(user, '_is_new', False)
    #     user.age = 60
    #     user.validate()
    #     self.assertTrue(isinstance(val['val'], ValidatingContext))
