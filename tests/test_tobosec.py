from __future__ import annotations
from datetime import datetime
from unittest import TestCase
from tests.classes.super_datetime import SuperDateTime

class TestTobosec(TestCase):

    def test_time_of_beginnig_of_second_value_is_datetime(self):
        d = SuperDateTime(dtbs=datetime(2021, 10, 11, 17, 37, 27, 446259))
        self.assertEqual(d.dtbs, datetime(2021,10, 11, 17, 37, 27))

    def test_time_of_beginnig_of_second_value_is_not_datetime(self):
        s = SuperDateTime(stbs="12345")
        self.assertEqual(s.stbs, "12345")
