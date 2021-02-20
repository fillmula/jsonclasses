from __future__ import annotations
from unittest import TestCase
from typing import Optional
from jsonclasses import jsonclass, ORMObject, types
from jsonclasses.exceptions import ValidationException
from jsonclasses.contexts import ValidatingContext


class TestCompareValidator(TestCase):

    def test_compare_will_not_trigger_if_object_is_new(self):

        val = {'val': 0}

        def compare(old: int, new: int):
            val['val'] = 1

        @jsonclass(class_graph='test_compare_1')
        class User(ORMObject):
            age: Optional[int] = types.int.compare(compare).required
        user = User(age=65)
        try:
            user.validate()
        except ValidationException:
            self.fail('compare should be fine if object is new')

    def test_compare_is_called_once_on_validate_if_object_is_modified_and_not_new(self):

        val = {'val': [0, 0]}
        time = {'time': 0}

        def compare(old: int, new: int):
            val['val'] = [old, new]
            time['time'] = time['time'] + 1

        @jsonclass(class_graph='test_compare_2')
        class User(ORMObject):
            age: Optional[int] = types.int.compare(compare).required
        user = User(age=65)
        setattr(user, '_is_new', False)
        user.age = 60
        user.validate()
        self.assertEqual(val, {'val': [65, 60]})
        self.assertEqual(time, {'time': 1})

    def test_compare_throws_if_callable_returns_a_string_2(self):

        def compare(old: int, new: int):
            return "invalid"

        @jsonclass(class_graph='test_compare_3')
        class User(ORMObject):
            age: Optional[int] = types.int.compare(compare).required
        user = User(age=1)
        setattr(user, '_is_new', False)
        user.age = 60
        self.assertRaisesRegex(ValidationException, 'invalid', user.validate)

    def test_compare_throws_if_callable_returns_a_string_3(self):

        def compare(old: int, new: int, key_path: str):
            return "invalid"

        @jsonclass(class_graph='test_compare_4')
        class User(ORMObject):
            age: Optional[int] = types.int.compare(compare).required
        user = User(age=1)
        setattr(user, '_is_new', False)
        user.age = 60
        self.assertRaisesRegex(ValidationException, 'invalid', user.validate)

    def test_compare_throws_if_callable_returns_a_string_4(self):

        def compare(old: int, new: int, key_path: str, obj: User):
            return "invalid"

        @jsonclass(class_graph='test_compare_5')
        class User(ORMObject):
            age: Optional[int] = types.int.compare(compare).required
        user = User(age=1)
        setattr(user, '_is_new', False)
        user.age = 60
        self.assertRaisesRegex(ValidationException, 'invalid', user.validate)

    def test_compare_throws_if_callable_returns_a_string_4(self):

        def compare(old: int, new: int, key_path: str, obj: User, context: ValidatingContext):
            return "invalid"

        @jsonclass(class_graph='test_compare_6')
        class User(ORMObject):
            age: Optional[int] = types.int.compare(compare).required
        user = User(age=1)
        setattr(user, '_is_new', False)
        user.age = 60
        self.assertRaisesRegex(ValidationException, 'invalid', user.validate)


    # def test_validate_throws__with_two_args_when_value_is_invalid(self):
    #     @jsonclass(class_graph='test_validate_4')
    #     class User(JSONObject):
    #         email: str = types.str.validate(lambda e, k: None if len(e) == 3 else f'totally wrong {k}').required
    #     user = User(email='abcd')
    #     self.assertRaisesRegex(ValidationException, 'totally wrong email', user.validate)

    # def test_validate_is_fine_with_three_args_when_value_is_valid(self):
    #     @jsonclass(class_graph='test_validate_5')
    #     class User(JSONObject):
    #         phone: str = '9'
    #         email: str = types.str.validate(lambda e, k, p: None if p.phone == '9' else f'totally wrong {k}').required
    #     user = User(email='abc')
    #     try:
    #         user.validate()
    #     except ValidationException:
    #         self.fail('validate should be fine if value is valid')

    # def test_validate_throws__with_three_args_when_value_is_invalid(self):
    #     @jsonclass(class_graph='test_validate_6')
    #     class User(JSONObject):
    #         phone: str = '9'
    #         email: str = types.str.validate(lambda e, k, p: None if p.phone != '9' else f'totally wrong {k}').required
    #     user = User(email='abcd')
    #     self.assertRaisesRegex(ValidationException, 'totally wrong email', user.validate)

    # def test_validate_is_fine_with_four_args_when_value_is_valid(self):
    #     @jsonclass(class_graph='test_validate_7')
    #     class User(JSONObject):
    #         phone: str = '9'
    #         email: str = types.str.validate(lambda e, k, p, c: None if c.root.phone == '9' else f'totally wrong {k}').required
    #     user = User(email='abc')
    #     try:
    #         user.validate()
    #     except ValidationException:
    #         self.fail('validate should be fine if value is valid')

    # def test_validate_throws__with_four_args_when_value_is_invalid(self):
    #     @jsonclass(class_graph='test_validate_8')
    #     class User(JSONObject):
    #         phone: str = '9'
    #         email: str = types.str.validate(lambda e, k, p, c: None if c.root.phone != '9' else f'totally wrong {k}').required
    #     user = User(email='abcd')
    #     self.assertRaisesRegex(ValidationException, 'totally wrong email', user.validate)
