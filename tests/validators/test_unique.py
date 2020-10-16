import unittest
from jsonclasses import jsonclass, JSONObject, types
from jsonclasses.exceptions import ValidationException
from datetime import datetime, date


class TestUniqueValidator(unittest.TestCase):

    def test_unique_is_fine_when_create_an_object(self):
        @jsonclass(class_graph='test_unique_1')
        class TestUser(JSONObject):
            password: str = types.str.writeonly.minlength(8).maxlength(16).transform(lambda p: p + '00xx').required
            phone_no: str
            username: str = types.str.writeonce.unique.required
            nickname: str = types.str.maxlength(30).required
            gender: str = types.str.writeonce.oneof(['male', 'female'])
            email: str = types.str.unique.required
        try:
            _user = TestUser()
        except ValidationException:
            self.fail('unique should not break things')

    def test_unique_shouldnt_break_things_and_remove_value(self):
        data = {
            "username": "john.qq",
            "nickname": "John QQ",
            "gender": "male",
            "email": "john.qq@wiosoftcrafts.com",
            "phoneNo": "+12345678"
        }

        @jsonclass(class_graph='test_unique_2')
        class User(JSONObject):
            username: str = types.str.writeonce.unique.required
            password: str = types.str.writeonly.minlength(8).maxlength(16).transform(lambda v: v + 'z').required
            nickname: str = types.str.maxlength(30).required
            gender: str = types.str.writeonce.oneof(['male', 'female'])
            email: str = types.str.unique.required
            phone_no: str
            wechat_open_id: str
        user = User(**data, password='1234567890')
        self.assertEqual(user.__fdict__, {
            'username': 'john.qq',
            'nickname': 'John QQ',
            'gender': 'male',
            'email': 'john.qq@wiosoftcrafts.com',
            'phone_no': '+12345678',
            'password': '1234567890z',
            'wechat_open_id': None
        })
