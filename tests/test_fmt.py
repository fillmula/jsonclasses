from __future__ import annotations
from datetime import date, datetime
from unittest import TestCase
from tests.classes.format import Format


class TestFmt(TestCase):

    def test_fmt_takes_callable_format(self):
        f = Format(color1='123456')
        self.assertEqual(f.tojson()['color1'], '#123456')
        self.assertEqual(f.color1, '123456')

    def test_fmt_takes_types_format(self):
        f = Format(color2='123456')
        self.assertEqual(f.tojson()['color2'], '#123456')
        self.assertEqual(f.color2, '123456')
