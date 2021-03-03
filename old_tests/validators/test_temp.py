from typing import Optional
from unittest import TestCase
from jsonclasses import jsonclass, ORMObject, types
from jsonclasses.exceptions import ValidationException


class TestTempValidator(TestCase):

    def test_temp_fields_do_not_go_to_json(self):
        @jsonclass(class_graph='test_temp_1')
        class User(ORMObject):
            phone: str
            auth_code: Optional[str] = types.str.temp
        user = User(phone='123456', auth_code='0502')
        self.assertEqual(user.phone, '123456')
        self.assertEqual(user.auth_code, '0502')
        json_dict = user.tojson()
        self.assertEqual(json_dict, {'phone': '123456'})

    def test_temp_fields_are_cleared_after_write(self):
        @jsonclass(class_graph='test_temp_2')
        class User(ORMObject):
            phone: str
            auth_code: Optional[str] = types.str.temp
        user = User(phone='123456', auth_code='0502')
        self.assertEqual(user.phone, '123456')
        self.assertEqual(user.auth_code, '0502')
        user._clear_temp_fields()
        self.assertEqual(user.phone, '123456')
        self.assertEqual(user.auth_code, None)

    def test_temp_fields_are_validated(self):
        @jsonclass(class_graph='test_temp_3')
        class User(ORMObject):
            phone: str
            auth_code: Optional[str] = types.str.temp.validate(lambda x: "wrong")
        user = User(phone='123456', auth_code='0502')
        with self.assertRaises(ValidationException) as context:
            user.validate()
        self.assertEqual(context.exception.keypath_messages['auth_code'], 'wrong')
