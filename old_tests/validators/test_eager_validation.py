import unittest
from typing import List, Dict
from jsonclasses import jsonclass, JSONObject, types
from jsonclasses.exceptions import ValidationException
from datetime import datetime, date


class TestEagerValidator(unittest.TestCase):

    def test_eager_validator_validates_on_init(self):
        @jsonclass(class_graph='test_eager_validator_1')
        class User(JSONObject):
            username: str = types.str.required
            password: str = types.str.minlength(8).maxlength(16).transform(lambda s: s + '0x0x').required
        with self.assertRaises(ValidationException) as context:
            _user = User(password='123')
            self.assertTrue("Value '123' at 'password' should have length not less than 8" in context.exception)

    def test_eager_validator_doesnt_cause_other_fields_to_validate_on_init(self):
        @jsonclass(class_graph='test_eager_validator_2')
        class User(JSONObject):
            username: str = types.str.required
            password: str = types.str.minlength(8).maxlength(10).transform(lambda s: s + '0x0x').required
        user = User(password='12345678')
        self.assertEqual(user.__fdict__, {'username': None, 'password': '123456780x0x'})

    def test_eager_validator_will_not_perform_when_value_is_none_on_init(self):
        @jsonclass(class_graph='test_eager_validator_3')
        class User(JSONObject):
            username: str = types.str.required
            password: str = types.str.minlength(8).maxlength(16).transform(lambda s: s + '0x0x').required
        try:
            _user = User()
        except ValidationException:
            self.fail('eager validator should not perform on init if value is None.')

    def test_eager_validator_validates_on_set(self):
        @jsonclass(class_graph='test_eager_validator_4')
        class User(JSONObject):
            username: str = types.str.required
            password: str = types.str.minlength(8).maxlength(16).transform(lambda s: s + '0x0x').required
        user = User()
        with self.assertRaises(ValidationException) as context:
            user.set(password='123')
            self.assertTrue("Value '123' at 'password' should have length not less than 8" in context.exception)

    def test_eager_validator_will_not_work_on_update(self):
        @jsonclass(class_graph='test_eager_validator_5')
        class User(JSONObject):
            username: str = types.str.required
            password: str = types.str.minlength(8).maxlength(16).transform(lambda s: s + '0x0x').required
        user = User()
        try:
            user.update(password='123')
        except ValidationException:
            self.fail('eager validator should not perform on update.')

    def test_eager_validator_prevents_validators_before_it_to_work_on_validate(self):
        @jsonclass(class_graph='test_eager_validator_6')
        class User(JSONObject):
            username: str = types.str.required
            password: str = types.str.minlength(2).maxlength(4).transform(lambda s: s + '0x0x').required
        user = User(username='john', password='1234')
        try:
            user.validate()
        except ValidationException:
            self.fail('eager validator should prevent validators before it to work on validate.')

    def test_eager_validator_should_validate_and_transform_inside_list(self):
        @jsonclass(class_graph='test_eager_validator_7')
        class User(JSONObject):
            passwords: List[str] = types.listof(
                types.str.minlength(2).maxlength(4).transform(lambda s: s + '0x0x0x0x')
            )
        try:
            _user = User(passwords=['123', '456', '789', '012'])
        except:
            self.fail('eager validator should not throw if value is valid')

    def test_eager_validator_should_validate_and_throw_inside_list(self):
        @jsonclass(class_graph='test_eager_validator_8')
        class User(JSONObject):
            passwords: List[str] = types.listof(
                types.str.minlength(2).maxlength(4).transform(lambda s: s + '0x0x0x0x')
            )
        with self.assertRaises(ValidationException):
            _user = User(passwords=['123xxx', '456xxx', '789xxx', '012xxx'])

    def test_eager_validator_should_validate_and_transform_inside_dict(self):
        @jsonclass(class_graph='test_eager_validator_9')
        class User(JSONObject):
            passwords: Dict[str, str] = types.dictof(
                types.str.minlength(2).maxlength(4).transform(lambda s: s + '0x0x0x0x')
            )
        try:
            _user = User(passwords={'a': '123', 'b': '456', 'c': '789', 'd': '012'})
        except:
            self.fail('eager validator should not throw if value is valid')

    def test_eager_validator_should_validate_and_throw_inside_dict(self):
        @jsonclass(class_graph='test_eager_validator_10')
        class User(JSONObject):
            passwords: Dict[str, str] = types.dictof(
                types.str.minlength(2).maxlength(4).transform(lambda s: s + '0x0x0x0x')
            )
        with self.assertRaises(ValidationException):
            _user = User(passwords={'a': '123xxx', 'b': '456xxx', 'c': '789xxx', 'd': '012xxx'})

    def test_eager_validator_should_validate_and_transform_inside_shape(self):
        @jsonclass(class_graph='test_eager_validator_11')
        class User(JSONObject):
            passwords: Dict[str, str] = types.shape({
                'a': types.str.minlength(2).maxlength(4).transform(lambda s: s + '0x0x0x0x'),
                'b': types.str.minlength(2).maxlength(4).transform(lambda s: s + '0x0x0x0x')
            })
        try:
            _user = User(passwords={'a': '123', 'b': '456'})
        except:
            self.fail('eager validator should not throw if value is valid')

    def test_eager_validator_should_validate_and_throw_inside_shape(self):
        @jsonclass(class_graph='test_eager_validator_12')
        class User(JSONObject):
            passwords: Dict[str, str] = types.shape({
                'a': types.str.minlength(2).maxlength(4).transform(lambda s: s + '0x0x0x0x'),
                'b': types.str.minlength(2).maxlength(4).transform(lambda s: s + '0x0x0x0x')
            })
        with self.assertRaises(ValidationException):
            _user = User(passwords={'a': '123xxx', 'b': '456xxx'})

    def test_eager_validator_should_lazy_validate_when_validate_inside_list(self):
        @jsonclass(class_graph='test_eager_validator_13')
        class User(JSONObject):
            passwords: List[str] = types.listof(
                types.str.minlength(2).maxlength(4).transform(lambda s: s + '0x0x0x0x')
            )
        user = User(passwords=['123', '456', '789', '012'])
        try:
            user.validate()
        except:
            self.fail('eager validator should not throw if not validation task after eager mark')

    def test_eager_validator_should_lazy_validate_when_validate_inside_dict(self):
        @jsonclass(class_graph='test_eager_validator_14')
        class User(JSONObject):
            passwords: Dict[str, str] = types.dictof(
                types.str.minlength(2).maxlength(4).transform(lambda s: s + '0x0x0x0x')
            )
        user = User(passwords={'a': '123', 'b': '456', 'c': '789', 'd': '012'})
        try:
            user.validate()
        except:
            self.fail('eager validator should not throw if not validation task after eager mark')

    def test_eager_validator_should_lazy_validate_when_validate_inside_shape(self):
        @jsonclass(class_graph='test_eager_validator_15')
        class User(JSONObject):
            passwords: Dict[str, str] = types.shape({
                'a': types.str.minlength(2).maxlength(4).transform(lambda s: s + '0x0x0x0x'),
                'b': types.str.minlength(2).maxlength(4).transform(lambda s: s + '0x0x0x0x')
            })
        user = User(passwords={'a': '123', 'b': '456'})
        try:
            user.validate()
        except:
            self.fail('eager validator should not throw if not validation task after eager mark')
