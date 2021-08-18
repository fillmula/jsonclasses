from __future__ import annotations
from unittest import TestCase
from tests.classes.cellphone_name import CellphoneName


class TestToCap(TestCase):

    def test_tocap_capitalize_simple_str(self):
        product = CellphoneName(cellphone_name='hello', cellphone_title='world')
        self.assertEqual(product.cellphone_name, 'Hello')

    def test_tocap_capitalize_str_contains_whitespace(self):
        product = CellphoneName(cellphone_name='hello world', cellphone_title='world')
        self.assertEqual(product.cellphone_name, 'Hello world')

    def test_tocap_capitalize_str_contains_int(self):
        product = CellphoneName(cellphone_name='hell1o world', cellphone_title='world')
        self.assertEqual(product.cellphone_name, 'Hell1o world')

    def test_tocap_capitalize_str_contains_special_character(self):
        product = CellphoneName(cellphone_name='hel!lo world', cellphone_title='world')
        self.assertEqual(product.cellphone_name, 'Hel!lo world')