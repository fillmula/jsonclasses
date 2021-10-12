from __future__ import annotations
from datetime import date, datetime
from unittest import TestCase
from tests.classes.super_datetime import SuperDateTime

class TestTonextyear(TestCase):

    def test_tonextyear_transforms_datetime_into_the_time_of_next_year(self):
        d = SuperDateTime(dtny=datetime(2021, 10, 11, 17, 37, 27, 446259))
        self.assertEqual(d.dtny, datetime(2022,1, 1, 0, 0))

    def test_tonextyear_transforms_date_into_the_time_of_next_year(self):
        d = SuperDateTime(dny=date(2021, 10, 11))
        self.assertEqual(d.dny, date(2022,1, 1))

    def test_tonextyear_does_not_transform_if_is_not_datetime_or_date(self):
        s = SuperDateTime(sny='12345')
        self.assertEqual(s.sny, '12345')
