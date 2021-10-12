from __future__ import annotations
from datetime import datetime
from unittest import TestCase
from tests.classes.super_datetime import SuperDateTime

class TestTonexthour(TestCase):

    def test_tonexthour_transforms_datetime_into_the_time_of_next_hour(self):
        d = SuperDateTime(dtnh=datetime(2021, 10, 11, 17, 37, 27, 446259))
        self.assertEqual(d.dtnh, datetime(2021,10, 11, 18, 0))

    def test_tonexthour_does_not_transform_if_is_not_datetime(self):
        s = SuperDateTime(stnh="12345")
        self.assertEqual(s.stnh, "12345")
