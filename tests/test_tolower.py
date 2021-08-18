from __future__ import annotations
from unittest import TestCase
from tests.classes.cellphone_description import CellphoneDescription


class TestToLower(TestCase):

    def test_convert_simple_str_to_lower_case(self):
        product = CellphoneDescription(cellphone_name='hello', cellphone_description='WORLD')
        self.assertEqual(product.cellphone_description, 'world')

    def test_convert_str_contains_whitespace_to_lower_case(self):
        product = CellphoneDescription(cellphone_name='hello', cellphone_description='WOR LD')
        self.assertEqual(product.cellphone_description, 'wor ld')


    def test_convert_str_contains_int_to_lower_case(self):
        product = CellphoneDescription(cellphone_name='hello', cellphone_description='WOR1LD')
        self.assertEqual(product.cellphone_description, 'wor1ld')

    def test_convert_str_contains_special_character_to_lower_case(self):
        product = CellphoneDescription(cellphone_name='hello', cellphone_description='WOR@LD#')
        self.assertEqual(product.cellphone_description, 'wor@ld#')