from unittest import TestCase
from jsonclasses import jsonclass, JSONObject, types
from jsonclasses.exceptions import ValidationException


class TestPresentWithValidator(TestCase):

    def test_presentwith_validator_throws_when_it_should_throw(self):
        @jsonclass(class_graph='test_presentwith_1')
        class User(JSONObject):
            calling_code: str = types.str.presentwith('phone_number')
            phone_number: str = types.str
        self.assertRaises(ValidationException, User(phone_number='1').validate)

    def test_presentwith_validator_dont_throw_when_it_shouldnt_throw(self):
        @jsonclass(class_graph='test_presentwith_2')
        class User(JSONObject):
            calling_code: str = types.str.presentwith('phone_number')
            phone_number: str = types.str
        User().validate()
