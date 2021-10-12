from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from tests.classes.product_with_alnum import AlnumProductCode


class TestAlnum(TestCase):

    def test_alnum_doesnt_raise_if_value_is_all_int(self):
        analysis = AlnumProductCode(product_name='water', product_code='12345')
        analysis.validate()

    def test_alnum_doesnt_raise_if_value_is_all_string(self):
        analysis = AlnumProductCode(product_name='water', product_code='aaaa')
        analysis.validate()

    def test_alnum_doesnt_raise_if_value_is_string_and_int(self):
        analysis = AlnumProductCode(product_name='water', product_code='aaaa123')
        analysis.validate()

    def test_alnum_raises_if_value_contains_dot(self):
        analysis = AlnumProductCode(product_name='water', product_code='aa1.12')
        with self.assertRaises(ValidationException) as context:
            analysis.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['productCode'],
                         "value is not alnum str")


    def test_alnum_raises_if_value_contains_special_character(self):
        analysis = AlnumProductCode(product_name='water', product_code='12a!')
        with self.assertRaises(ValidationException) as context:
            analysis.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['productCode'],
                         "value is not alnum str")
