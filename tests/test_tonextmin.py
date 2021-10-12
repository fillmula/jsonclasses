from __future__ import annotations
from datetime import datetime
from unittest import TestCase
from tests.classes.super_datetime import SuperDateTime

class TestTonextmin(TestCase):

    def test_tonextmin_transforms_datetime_into_the_time_of_next_minute(self):
        d = SuperDateTime(dtnm=datetime(2021, 10, 11, 17, 37, 27, 446259))
        self.assertEqual(d.dtnm, datetime(2021,10, 11, 17, 38))

    def test_tonextmin_does_not_transform_if_is_not_datetime(self):
        s = SuperDateTime(stnm="12345")
        self.assertEqual(s.stnm, "12345")
