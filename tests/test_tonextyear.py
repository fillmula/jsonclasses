from __future__ import annotations
from datetime import date, datetime
from unittest import TestCase
from tests.classes.super_datetime import SuperDateTime

class TestTonextyear(TestCase):

    def test_tonextyear_time_of_next_year_value_is_datetime(self):
        d = SuperDateTime(dtny=datetime(2021, 10, 11, 17, 37, 27, 446259))
        self.assertEqual(d.dtny, datetime(2022,1, 1, 0, 0))

    def test_tonextyear_time_of_next_year_value_is_date(self):
        d = SuperDateTime(dny=date(2021, 10, 11))
        self.assertEqual(d.dny, date(2022,1, 1))

    def test_tonextyear_time_of_next_year_value_is_not_datetime_and_not_date(self):
        s = SuperDateTime(sny='12345')
        self.assertEqual(s.sny, '12345')
