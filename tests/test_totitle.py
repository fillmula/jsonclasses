from __future__ import annotations
from unittest import TestCase
from tests.classes.cellphone_title import CellphoneTitle


class TestToTitle(TestCase):

    def test_totitle_titlizes_srt(self):
        product = CellphoneTitle(cellphone_name='hello', cellphone_title='sale for today')
        self.assertEqual(product.cellphone_title, 'Sale For Today')

    def test_totitle_titlizes_srt_with_special_characters(self):
        product = CellphoneTitle(cellphone_name='hello', cellphone_title='#sale !!$for t*^oday')
        self.assertEqual(product.cellphone_title, '#Sale !!$For T*^Oday')

    def test_totitle_titlizes_srt_with_int(self):
        product = CellphoneTitle(cellphone_name='hello', cellphone_title='123sale 2323for t77oday')
        self.assertEqual(product.cellphone_title, '123Sale 2323For T77Oday')