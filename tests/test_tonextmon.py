from __future__ import annotations
from datetime import date, datetime
from unittest import TestCase
from tests.classes.super_datetime import SuperDateTime

class TestTonextmon(TestCase):

    def test_tonextmon_transforms_datetime_into_the_time_of_next_month(self):
        d = SuperDateTime(dtnmth=datetime(2021, 10, 11, 17, 37, 27, 446259))
        self.assertEqual(d.dtnmth, datetime(2021,11, 1, 0, 0))

    def test_tonextmon_transforms_date_into_the_time_of_next_month(self):
        d = SuperDateTime(dnmth=date(2021, 10, 11))
        self.assertEqual(d.dnmth, date(2021,11, 1))

    def test_tonextmon_does_not_transform_if_is_not_datetime_or_date(self):
        s = SuperDateTime(snmth='12345')
        self.assertEqual(s.snmth, '12345')
