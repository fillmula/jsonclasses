from __future__ import annotations
from unittest import TestCase
from jsonclasses.exceptions import ValidationException
from tests.classes.enum_user import Gender, EnumUser
from tests.classes.value_gender_user import ValueGender, ValueGenderUser
from tests.classes.lname_gender_user import LnameGender, LnameGenderUser


class TestEnum(TestCase):

    def test_enum_is_enum_after_assigned(self):
        user = EnumUser(name='Kiên Kiong', gender=Gender.MALE)
        self.assertEqual(user._data_dict,
                         {'name': 'Kiên Kiong', 'gender': Gender.MALE})

    def test_enum_assign_raises_if_value_is_not_valid_enum_value(self):
        with self.assertRaises(ValidationException) as context:
            EnumUser(name='Kiên Kiong', gender=8)
        self.assertEqual(context.exception.keypath_messages['gender'],
                         "unknown enum value")

    def test_enum_accepts_uppercase_name_on_assign_by_default(self):
        user = EnumUser(name='Kiên Kiong', gender='MALE')
        self.assertEqual(user._data_dict,
                         {'name': 'Kiên Kiong', 'gender': Gender.MALE})

    def test_enum_does_not_accept_lowercase_name_on_assign_by_default(self):
        with self.assertRaises(ValidationException) as context:
            EnumUser(name='Kiên Kiong', gender='male')
        self.assertEqual(context.exception.keypath_messages['gender'],
                         "unknown enum value")

    def test_enum_raises_if_value_is_not_valid_enum_value(self):
        user = EnumUser(name='Kiên Kiong', gender='MALE')
        user.gender = 6
        with self.assertRaises(ValidationException) as context:
            user.validate()
        self.assertEqual(context.exception.keypath_messages['gender'],
                         "invalid enum value")

    def test_enum_raises_if_value_is_not_the_same_enum(self):
        user = EnumUser(name='Kiên Kiong', gender='MALE')
        user.gender = LnameGender.MALE
        with self.assertRaises(ValidationException) as context:
            user.validate()
        self.assertEqual(context.exception.keypath_messages['gender'],
                         "invalid enum value")

    def test_enum_outputs_to_uppercase_name_by_default(self):
        user = EnumUser(name='Nng Li', gender=Gender.MALE)
        self.assertEqual(user.tojson(),
                         {'name': 'Nng Li', 'gender': 'MALE'})

    def test_enum_accept_value_if_specified(self):
        user = ValueGenderUser(name='Mia', gender=1)
        self.assertEqual(user._data_dict,
                         {'name': 'Mia', 'gender': ValueGender.MALE})

    def test_enum_accept_lowercase_name_if_specified(self):
        user = LnameGenderUser(name='Mia', gender='male')
        self.assertEqual(user._data_dict,
                         {'name': 'Mia', 'gender': LnameGender.MALE})

    def test_enum_outputs_to_value_if_specified(self):
        user = ValueGenderUser(name='Nng Li', gender=ValueGender.MALE)
        self.assertEqual(user.tojson(),
                         {'name': 'Nng Li', 'gender': 1})

    def test_enum_outputs_to_lowercase_name_if_specified(self):
        user = LnameGenderUser(name='Nng Li', gender=LnameGender.MALE)
        self.assertEqual(user.tojson(),
                         {'name': 'Nng Li', 'gender': 'male'})
