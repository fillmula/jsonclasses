from __future__ import annotations
from unittest import TestCase
from tests.classes.cellphone_detail import CellphoneDetail


class TestToUpper(TestCase):

    def test_convert_simple_str_to_upper_case(self):
        product = CellphoneDetail(cellphone_name='hello', cellphone_detail='world')
        self.assertEqual(product.cellphone_detail, 'WORLD')

    def test_convert_str_contains_whitespace_to_upper_case(self):
        product = CellphoneDetail(cellphone_name='hello', cellphone_detail='wor ld')
        self.assertEqual(product.cellphone_detail, 'WOR LD')


    def test_convert_str_contains_int_to_upper_case(self):
        product = CellphoneDetail(cellphone_name='hello', cellphone_detail='wor1ld')
        self.assertEqual(product.cellphone_detail, 'WOR1LD')

    def test_convert_str_contains_special_character_to_upper_case(self):
        product = CellphoneDetail(cellphone_name='hello', cellphone_detail='wor@ld#')
        self.assertEqual(product.cellphone_detail, 'WOR@LD#')