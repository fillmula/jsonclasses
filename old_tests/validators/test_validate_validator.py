import unittest
from jsonclasses import jsonclass, JSONObject, types
from jsonclasses.exceptions import ValidationException


class TestValidateValidator(unittest.TestCase):

    def test_validate_is_fine_when_value_is_valid(self):
        @jsonclass(class_graph='test_validate_1')
        class User(JSONObject):
            email: str = types.str.validate(lambda e: None if len(e) == 3 else 'totally wrong').required
        user = User(email='abc')
        try:
            user.validate()
        except ValidationException:
            self.fail('validate should be fine if value is valid')

    def test_validate_throws_when_value_is_invalid(self):
        @jsonclass(class_graph='test_validate_2')
        class User(JSONObject):
            email: str = types.str.validate(lambda e: None if len(e) == 3 else 'totally wrong').required
        user = User(email='abcd')
        self.assertRaisesRegex(ValidationException, 'totally wrong', user.validate)

    def test_validate_is_fine_with_two_args_when_value_is_valid(self):
        @jsonclass(class_graph='test_validate_3')
        class User(JSONObject):
            email: str = types.str.validate(lambda e, k: None if len(e) == 3 else f'totally wrong {k}').required
        user = User(email='abc')
        try:
            user.validate()
        except ValidationException:
            self.fail('validate should be fine if value is valid')

    def test_validate_throws__with_two_args_when_value_is_invalid(self):
        @jsonclass(class_graph='test_validate_4')
        class User(JSONObject):
            email: str = types.str.validate(lambda e, k: None if len(e) == 3 else f'totally wrong {k}').required
        user = User(email='abcd')
        self.assertRaisesRegex(ValidationException, 'totally wrong email', user.validate)

    def test_validate_is_fine_with_three_args_when_value_is_valid(self):
        @jsonclass(class_graph='test_validate_5')
        class User(JSONObject):
            phone: str = '9'
            email: str = types.str.validate(lambda e, k, p: None if p.phone == '9' else f'totally wrong {k}').required
        user = User(email='abc')
        try:
            user.validate()
        except ValidationException:
            self.fail('validate should be fine if value is valid')

    def test_validate_throws__with_three_args_when_value_is_invalid(self):
        @jsonclass(class_graph='test_validate_6')
        class User(JSONObject):
            phone: str = '9'
            email: str = types.str.validate(lambda e, k, p: None if p.phone != '9' else f'totally wrong {k}').required
        user = User(email='abcd')
        self.assertRaisesRegex(ValidationException, 'totally wrong email', user.validate)

    def test_validate_is_fine_with_four_args_when_value_is_valid(self):
        @jsonclass(class_graph='test_validate_7')
        class User(JSONObject):
            phone: str = '9'
            email: str = types.str.validate(lambda e, k, p, c: None if c.root.phone == '9' else f'totally wrong {k}').required
        user = User(email='abc')
        try:
            user.validate()
        except ValidationException:
            self.fail('validate should be fine if value is valid')

    def test_validate_throws__with_four_args_when_value_is_invalid(self):
        @jsonclass(class_graph='test_validate_8')
        class User(JSONObject):
            phone: str = '9'
            email: str = types.str.validate(lambda e, k, p, c: None if c.root.phone != '9' else f'totally wrong {k}').required
        user = User(email='abcd')
        self.assertRaisesRegex(ValidationException, 'totally wrong email', user.validate)
