from __future__ import annotations
from datetime import datetime
from unittest import TestCase
from tests.classes.super_datetime import SuperDateTime

class TestTonextsec(TestCase):

    def test_tonextsec_time_of_next_second_value_is_datetime(self):
        d = SuperDateTime(dtns=datetime(2021, 10, 11, 17, 37, 27, 446259))
        self.assertEqual(d.dtns, datetime(2021,10, 11, 17, 37, 28))

    def test_tonextsec_time_of_next_second_value_is_not_datetime(self):
        s = SuperDateTime(stns="12345")
        self.assertEqual(s.stns, "12345")
