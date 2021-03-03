import unittest
from jsonclasses import jsonclass, JSONObject, types
from jsonclasses.exceptions import ValidationException


class TestLengthValidator(unittest.TestCase):

    def test_length_of_value_should_be_in_between(self):
        @jsonclass(class_graph='test_length_1')
        class Secret(JSONObject):
            password: str = types.str.length(2, 4)
        try:
            Secret(password='123').validate()
        except:
            self.fail('length of value in between should not throw')

    def test_length_of_value_should_be_fine_when_same_as_min(self):
        @jsonclass(class_graph='test_length_2')
        class Secret(JSONObject):
            password: str = types.str.length(2, 4)
        try:
            Secret(password='12').validate()
        except:
            self.fail('length of value when is min should not throw')

    def test_length_of_value_should_be_fine_when_same_as_max(self):
        @jsonclass(class_graph='test_length_3')
        class Secret(JSONObject):
            password: str = types.str.length(2, 4)
        try:
            Secret(password='1234').validate()
        except:
            self.fail('length of value when is max should not throw')

    def test_length_of_value_should_be_definitely_the_same_as_length_if_only_one_arg_is_provided(self):
        @jsonclass(class_graph='test_length_4')
        class Secret(JSONObject):
            password: str = types.str.length(2)
        try:
            Secret(password='12').validate()
        except:
            self.fail('length of value should be ok when it has the exact length as the only provided arg')

    def test_length_should_raise_if_value_length_is_smaller_than_min(self):
        @jsonclass(class_graph='test_length_5')
        class Secret(JSONObject):
            password: str = types.str.length(2, 4)
        secret = Secret(password='1')
        self.assertRaises(ValidationException, secret.validate)

    def test_length_should_raise_if_value_length_is_larger_than_max(self):
        @jsonclass(class_graph='test_length_6')
        class Secret(JSONObject):
            password: str = types.str.length(2, 4)
        secret = Secret(password='55555')
        self.assertRaises(ValidationException, secret.validate)

    def test_length_should_raise_if_value_length_is_different_than_only_arg(self):
        @jsonclass(class_graph='test_length_7')
        class Secret(JSONObject):
            password: str = types.str.length(5)
        secret = Secret(password='666666')
        self.assertRaises(ValidationException, secret.validate)
