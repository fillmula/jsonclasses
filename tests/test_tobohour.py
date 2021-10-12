from __future__ import annotations
from datetime import datetime
from unittest import TestCase

from tests.classes.super_datetime import SuperDateTime


class TestTobosec(TestCase):

    def test_time_of_beginning_of_hours_by_replace(self):
        d = SuperDateTime(dtbh=datetime(2021, 10, 11, 17, 37, 27))
        self.assertEqual(d.dtbh, datetime(2021,10, 11, 17, 0))

    def test_time_of_beginnig_of_hour_value_is_not_datetime(self):
        s = SuperDateTime(stbh="12345")
        self.assertEqual(s.stbh, "12345")
