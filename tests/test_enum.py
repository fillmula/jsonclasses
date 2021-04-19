from __future__ import annotations
from unittest import TestCase
from jsonclasses.exceptions import ValidationException
from tests.classes.enum_user import Gender, EnumUser


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

    def test_enum_raises_if_value_is_not_valid_enum_value(self):
        user = EnumUser(name='Kiên Kiong', gender='MALE')
        user.gender = 6
        with self.assertRaises(ValidationException) as context:
            user.validate()
        self.assertEqual(context.exception.keypath_messages['gender'],
                         "invalid enum value")

    def test_enum_outputs_to_uppercase_name_by_default(self):
        user = EnumUser(name='Nng Li', gender=Gender.MALE)
        self.assertEqual(user.tojson(),
                         {'name': 'Nng Li', 'gender': 'MALE'})
