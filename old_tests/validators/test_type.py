import unittest
from jsonclasses import jsonclass, JSONObject, types
from jsonclasses.exceptions import ValidationException
from datetime import datetime, date


class TestTypeValidators(unittest.TestCase):

    def test_str_validator_dont_raise(self):
        @jsonclass(class_graph='test_type_str_n')
        class Secret(JSONObject):
            secret: str = types.str
        secret = Secret(secret='2')
        secret.validate()

    def test_str_validator_raises(self):
        @jsonclass(class_graph='test_type_str_y')
        class Secret(JSONObject):
            secret: str = types.str
        secret = Secret(secret=5)
        self.assertRaises(ValidationException, secret.validate)

    def test_int_validator_dont_raise(self):
        @jsonclass(class_graph='test_type_int_n')
        class Secret(JSONObject):
            secret: int = types.int
        secret = Secret(secret=5)
        secret.validate()

    def test_int_validator_raises(self):
        @jsonclass(class_graph='test_type_int_y')
        class Secret(JSONObject):
            secret: int = types.int
        secret = Secret(secret='5')
        self.assertRaises(ValidationException, secret.validate)

    def test_float_validator_dont_raise(self):
        @jsonclass(class_graph='test_type_float_n')
        class Secret(JSONObject):
            secret: float = types.float
        secret = Secret(secret=5.3)
        secret.validate()

    def test_float_validator_raises(self):
        @jsonclass(class_graph='test_type_float_y')
        class Secret(JSONObject):
            secret: float = types.float
        secret = Secret(secret='5')
        self.assertRaises(ValidationException, secret.validate)

    def test_bool_validator_dont_raise(self):
        @jsonclass(class_graph='test_type_bool_n')
        class Secret(JSONObject):
            secret: bool = types.bool
        secret = Secret(secret=True)
        secret.validate()

    def test_bool_validator_raises(self):
        @jsonclass(class_graph='test_type_bool_y')
        class Secret(JSONObject):
            secret: bool = types.bool
        secret = Secret(secret='5')
        self.assertRaises(ValidationException, secret.validate)

    def test_date_validator_dont_raise(self):
        @jsonclass(class_graph='test_type_date_n')
        class Secret(JSONObject):
            secret: date = types.date
        secret = Secret(secret=date(2020, 9, 30))
        secret.validate()

    def test_date_create_raises(self):
        @jsonclass(class_graph='test_type_date_cy')
        class Secret(JSONObject):
            secret: date = types.date
        with self.assertRaises(ValidationException):
            Secret(secret='5')

    def test_date_validator_raises(self):
        @jsonclass(class_graph='test_type_date_y')
        class Secret(JSONObject):
            secret: date = types.date
        secret = Secret(secret=date(2020, 9, 30))
        secret.secret = "4"
        self.assertRaises(ValidationException, secret.validate)

    def test_datetime_validator_dont_raise(self):
        @jsonclass(class_graph='test_type_datetime_n')
        class Secret(JSONObject):
            secret: datetime = types.datetime
        secret = Secret(secret=datetime(2020, 9, 30))
        secret.validate()

    def test_datetime_create_raises(self):
        @jsonclass(class_graph='test_type_datetime_cy')
        class Secret(JSONObject):
            secret: datetime = types.datetime
        with self.assertRaises(ValidationException):
            Secret(secret='5')

    def test_datetime_validator_raises(self):
        @jsonclass(class_graph='test_type_datetime_y')
        class Secret(JSONObject):
            secret: datetime = types.datetime
        secret = Secret(secret=datetime(2020, 9, 30))
        secret.secret = "4"
        self.assertRaises(ValidationException, secret.validate)
