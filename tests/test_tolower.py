from __future__ import annotations
from unittest import TestCase
from tests.classes.cellphone_description import CellphoneDescription


class TestToLower(TestCase):

    def test_tolower_lowercasefies_str(self):
        product = CellphoneDescription(cellphone_name='hello', cellphone_description='WORLD')
        self.assertEqual(product.cellphone_description, 'world')

    def test_tolower_lowercasefies_str_with_whitespace(self):
        product = CellphoneDescription(cellphone_name='hello', cellphone_description='WOR LD')
        self.assertEqual(product.cellphone_description, 'wor ld')


    def test_tolower_lowercasefies_str_with_int(self):
        product = CellphoneDescription(cellphone_name='hello', cellphone_description='WOR1LD')
        self.assertEqual(product.cellphone_description, 'wor1ld')

    def test_tolower_lowercasefies_str_with_special_characters(self):
        product = CellphoneDescription(cellphone_name='hello', cellphone_description='WOR@LD#')
        self.assertEqual(product.cellphone_description, 'wor@ld#')
