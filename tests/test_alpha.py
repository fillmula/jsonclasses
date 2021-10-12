from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from tests.classes.product_name import AlphaProductName


class TestIsAlpha(TestCase):

    def test_alpha_doesnt_raise_if_value_is_alpha(self):
        analysis = AlphaProductName(product_name='water')
        analysis.validate()

    def test_alpha_raises_if_value_is_number(self):
        analysis = AlphaProductName(product_name='123')
        with self.assertRaises(ValidationException) as context:
            analysis.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['productName'],
                         "value is not alpha str")

    def test_alpha_raises_if_value_contains_number(self):
        analysis = AlphaProductName(product_name='water12')
        with self.assertRaises(ValidationException) as context:
            analysis.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['productName'],
                         "value is not alpha str")

    def test_alpha_raises_if_value_contains_special_character(self):
        analysis = AlphaProductName(product_name='water!')
        with self.assertRaises(ValidationException) as context:
            analysis.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['productName'],
                         "value is not alpha str")
