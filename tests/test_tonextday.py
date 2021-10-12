from __future__ import annotations
from datetime import date, datetime
from unittest import TestCase
from tests.classes.super_datetime import SuperDateTime

class TestTonextday(TestCase):

    def test_tonextday_time_of_next_day_value_is_datetime(self):
        d = SuperDateTime(dtnd=datetime(2021, 10, 11, 17, 37, 27, 446259))
        self.assertEqual(d.dtnd, datetime(2021,10, 12, 0, 0))

    def test_tonextday_time_of_next_day_value_is_date(self):
        d = SuperDateTime(dnd=date(2021, 10, 11))
        self.assertEqual(d.dnd, date(2021,10, 12))

    def test_tonextday_time_of_next_day_value_is_not_datetime_and_not_date(self):
        s = SuperDateTime(snd='12345')
        self.assertEqual(s.snd, '12345')
