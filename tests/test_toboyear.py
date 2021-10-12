from __future__ import annotations
from datetime import date, datetime
from unittest import TestCase

from tests.classes.super_datetime import SuperDateTime


class TestToboyear(TestCase):

    def test_toboyear_time_of_beginning_of_year_is_datetime(self):
        d = SuperDateTime(dtby=datetime(2021, 10, 11, 17, 37, 27,43235))
        self.assertEqual(d.dtby, datetime(2021,1, 1, 0, 0))

    def test_toboyear_time_of_beginning_of_year_is_date(self):
        d = SuperDateTime(dby=date(2021, 10, 11))
        self.assertEqual(d.dby, date(2021,1, 1))

    def test_toboyear_time_of_beginnig_of_year_value_is_not_datetime(self):
        s = SuperDateTime(sby="12345")
        self.assertEqual(s.sby, "12345")
