from __future__ import annotations
from unittest import TestCase
from jsonclasses.exceptions import ValidationException
from tests.classes.product_with_digit import DigitAnalysis


class TestDigit(TestCase):

    def test_digit_doesnt_raise_if_value_is_digit(self):
        analysis = DigitAnalysis(product_name='water', product_id='12345')
        analysis.validate()

    def test_digit_raises_if_value_is_value_is_float(self):
        analysis = DigitAnalysis(product_name='water', product_id='12.1')
        with self.assertRaises(ValidationException) as context:
            analysis.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['product_id'],
                         "product_id '12.1' at 'product_id' is not a digit.")

    def test_digit_raises_if_value_is_value_contains_alphabet(self):
        analysis = DigitAnalysis(product_name='water', product_id='12a')
        with self.assertRaises(ValidationException) as context:
            analysis.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['product_id'],
                         "product_id '12a' at 'product_id' is not a digit.")

    def test_digit_raises_if_value_is_value_with_special_character(self):
        analysis = DigitAnalysis(product_name='water', product_id='12!')
        with self.assertRaises(ValidationException) as context:
            analysis.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['product_id'],
                         "product_id '12!' at 'product_id' is not a digit.")