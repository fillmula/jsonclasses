from __future__ import annotations
from datetime import date, datetime
from unittest import TestCase

from tests.classes.super_datetime import SuperDateTime


class TestTobomon(TestCase):

    def test_tobomon_transforms_datetime_into_the_time_of_beginning_of_month(self):
        d = SuperDateTime(dtbmth=datetime(2021, 10, 11, 17, 37, 27,43235))
        self.assertEqual(d.dtbmth, datetime(2021,10, 1, 0, 0))

    def test_tobomon_transforms_date_into_the_time_of_beginning_of_month(self):
        d = SuperDateTime(dbmth=date(2021, 10, 11))
        self.assertEqual(d.dbmth, date(2021,10, 1))

    def test_tobomon_does_not_transform_if_is_not_datetime(self):
        s = SuperDateTime(sbmth="12345")
        self.assertEqual(s.sbmth, "12345")
