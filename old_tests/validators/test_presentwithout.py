from unittest import TestCase
from jsonclasses import jsonclass, JSONObject, types
from jsonclasses.exceptions import ValidationException


class TestPresentWithoutValidator(TestCase):

    def test_presentwithout_validator_throws_when_it_should_throw_single(self):
        @jsonclass(class_graph='test_presentwithout_1')
        class User(JSONObject):
            email: str = types.str.presentwithout('phone_number')
            phone_number: str = types.str.presentwithout('email')
        self.assertRaises(ValidationException, User().validate)

    def test_presentwith_validator_dont_throw_when_it_shouldnt_throw_single(self):
        @jsonclass(class_graph='test_presentwithout_2')
        class User(JSONObject):
            email: str = types.str.presentwithout('phone_number')
            phone_number: str = types.str.presentwithout('email')
        User(email='a@g.com').validate()
        User(phone_number='a@g.com').validate()

    def test_presentwithout_validator_throws_when_it_should_throw_multiple(self):
        @jsonclass(class_graph='test_presentwithout_3')
        class User(JSONObject):
            a: str = types.str.presentwithout(['b', 'c'])
            b: str = types.str.presentwithout(['a', 'c'])
            c: str = types.str.presentwithout(['b', 'c'])
        self.assertRaises(ValidationException, User().validate)

    def test_presentwith_validator_dont_throw_when_it_shouldnt_throw_multiple(self):
        @jsonclass(class_graph='test_presentwithout_4')
        class User(JSONObject):
            a: str = types.str.presentwithout(['b', 'c'])
            b: str = types.str.presentwithout(['a', 'c'])
            c: str = types.str.presentwithout(['a', 'b'])
        User(a='a').validate()
        User(b='a').validate()
        User(c='a').validate()
