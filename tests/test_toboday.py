from __future__ import annotations
from datetime import date, datetime
from unittest import TestCase

from tests.classes.super_datetime import SuperDateTime


class TestToboday(TestCase):

    def test_toboday_transforms_datetime_into_the_time_of_beginning_of_day(self):
        d = SuperDateTime(dtbd=datetime(2021, 10, 11, 17, 37, 27,43235))
        self.assertEqual(d.dtbd, datetime(2021,10, 11, 0, 0))

    def test_toboday_transforms_date_into_the_time_of_beginning_of_day(self):
        d = SuperDateTime(dbd=date(2021, 10, 11))
        self.assertEqual(d.dbd, date(2021,10, 11))

    def test_toboday_does_not_transform_if_is_not_datetime(self):
        s = SuperDateTime(sbd="12345")
        self.assertEqual(s.sbd, "12345")
