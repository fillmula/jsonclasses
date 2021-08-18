from __future__ import annotations
from unittest import TestCase
from jsonclasses.exceptions import ValidationException
from tests.classes.product_with_alnum import AlnumAnalysis


class TestAlum(TestCase):

    def test_alum_doesnt_raise_if_value_is_all_digit(self):
        analysis = AlnumAnalysis(product_name='water', product_code='12345')
        analysis.validate()

    def test_alum_doesnt_raise_if_value_is_all_string(self):
        analysis = AlnumAnalysis(product_name='water', product_code='aaaa')
        analysis.validate()

    def test_alum_doesnt_raise_if_value_is_alnum(self):
        analysis = AlnumAnalysis(product_name='water', product_code='aaaa123')
        analysis.validate()

    def test_alnum_raises_if_value_is_value_contains_dot(self):
        analysis = AlnumAnalysis(product_name='water', product_code='aa1.12')
        with self.assertRaises(ValidationException) as context:
            analysis.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['product_code'],
                         "product_code 'aa1.12' at 'product_code' is not made up of alpha and number.")


    def test_alnum_raises_if_value_contains_special_character(self):
        analysis = AlnumAnalysis(product_name='water', product_code='12a!')
        with self.assertRaises(ValidationException) as context:
            analysis.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['product_code'],
                         "product_code '12a!' at 'product_code' is not made up of alpha and number.")