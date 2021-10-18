from __future__ import annotations
from tests.classes.super_str import SuperStr
from unittest import TestCase



class TestPadStart(TestCase):

    def test_padstart_adds_str_to_the_start_of_str(self):
        ps = SuperStr(pads="aaaaa")
        self.assertEqual(ps.pads, "sssssaaaaa")

    def test_padstart_keeps_value_when_type_of_value_is_not_str(self):
        ps = SuperStr(padis=80)
        self.assertEqual(ps.padis, 80)

    def test_padstart_keeps_value_when_target_length_less_value_length(self):
        ps = SuperStr(pads="aaaaaaaaaaa")
        self.assertEqual(ps.pads, "aaaaaaaaaaa")

    def test_padstart_adds_callable_to_the_start_of_str(self):
        ps = SuperStr(c_pads="aaaaa")
        self.assertEqual(ps.c_pads, "sssssaaaaa")

    def test_padstart_adds_types_to_the_start_of_str(self):
        ps = SuperStr(t_pads="aaaaa")
        self.assertEqual(ps.t_pads, "sssssaaaaa")
