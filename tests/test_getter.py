from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from tests.classes.calc_user import CalcUser


class TestGetter(TestCase):

    def test_getter_gets_correct_value(self):
        user = CalcUser(name="Peter Layber", base_score=25.54)
        self.assertEqual(user.first_name, 'Peter')
        self.assertEqual(user.last_name, 'Layber')
        self.assertAlmostEqual(user.score, 51.08)
        self.assertEqual(user._data_dict,
                         {'name': 'Peter Layber', 'base_score': 25.54})

    def test_calc_fields_can_be_output_to_json(self):
        user = CalcUser(name="Peter Layber", base_score=25.54)
        result = user.tojson()
        self.assertEqual(result, {'name': 'Peter Layber',
                                  'firstName': 'Peter',
                                  'lastName': 'Layber',
                                  'score': 51.08,
                                  'baseScore': 25.54})

    def test_calc_fields_can_be_validated(self):
        user = CalcUser(name="Peter Layber", base_score=25.54)
        with self.assertRaises(ValidationException) as context:
            user.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['score'],
                         "value is not negative")
