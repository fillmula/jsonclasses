from __future__ import annotations
from unittest import TestCase
from tests.classes.cellphone_detail import CellphoneDetail


class TestToUpper(TestCase):

    def test_toupper_uppercasefies_str(self):
        product = CellphoneDetail(cellphone_name='hello', cellphone_detail='world')
        self.assertEqual(product.cellphone_detail, 'WORLD')

    def test_toupper_uppercasefies_str_with_whitespace(self):
        product = CellphoneDetail(cellphone_name='hello', cellphone_detail='wor ld')
        self.assertEqual(product.cellphone_detail, 'WOR LD')


    def test_toupper_uppercasefies_str_with_int(self):
        product = CellphoneDetail(cellphone_name='hello', cellphone_detail='wor1ld')
        self.assertEqual(product.cellphone_detail, 'WOR1LD')

    def test_toupper_uppercasefies_str_with_special_characters(self):
        product = CellphoneDetail(cellphone_name='hello', cellphone_detail='wor@ld#')
        self.assertEqual(product.cellphone_detail, 'WOR@LD#')