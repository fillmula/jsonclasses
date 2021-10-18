from __future__ import annotations
from tests.classes.super_str import SuperStr
from unittest import TestCase



class TestPadEnd(TestCase):

    def test_padend_adds_str_to_the_end_of_str(self):
        ps = SuperStr(pade="aaaaa")
        self.assertEqual(ps.pade, "aaaaaeeeee")

    def test_padend_keeps_value_when_type_of_value_is_not_str(self):
        ps = SuperStr(padie=80)
        self.assertEqual(ps.padie, 80)

    def test_padend_keeps_value_when_target_length_less_value_length(self):
        ps = SuperStr(pade="aaaaaaaaaaa")
        self.assertEqual(ps.pade, "aaaaaaaaaaa")

    def test_padend_adds_callable_str_to_the_end_of_str(self):
        ps = SuperStr(padce="aaaaa")
        self.assertEqual(ps.padce, "aaaaaeeeee")

    def test_padend_adds_types_str_to_the_end_of_str(self):
        ps = SuperStr(padte="aaaaa")
        self.assertEqual(ps.padte, "aaaaaeeeee")
