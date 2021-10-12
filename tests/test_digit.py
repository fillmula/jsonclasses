from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from tests.classes.product_with_digit import DigitProductId


class TestDigit(TestCase):

    def test_digit_doesnt_raise_if_value_is_digit(self):
        analysis = DigitProductId(product_name='water', product_id='12345')
        analysis.validate()

    def test_digit_raises_if_value_is_float(self):
        analysis = DigitProductId(product_name='water', product_id='12.1')
        with self.assertRaises(ValidationException) as context:
            analysis.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['productId'],
                         "value is not digit string")

    def test_digit_raises_if_value_contains_alphabet(self):
        analysis = DigitProductId(product_name='water', product_id='12a')
        with self.assertRaises(ValidationException) as context:
            analysis.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['productId'],
                         "value is not digit string")

    def test_digit_raises_if_value_contains_special_character(self):
        analysis = DigitProductId(product_name='water', product_id='12!')
        with self.assertRaises(ValidationException) as context:
            analysis.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['productId'],
                         "value is not digit string")
