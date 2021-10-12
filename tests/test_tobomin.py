from __future__ import annotations
from datetime import datetime
from unittest import TestCase
from tests.classes.super_datetime import SuperDateTime

class TestTobomin(TestCase):

    def test_tobomin_transforms_datetime_into_the_time_of_beginning_of_minute(self):
        d = SuperDateTime(dtbm=datetime(2021, 10, 11, 17, 37, 27))
        self.assertEqual(d.dtbm, datetime(2021,10, 11, 17, 37))

    def test_tobomin_does_not_transform_if_is_not_datetime(self):
        s = SuperDateTime(stbm="12345")
        self.assertEqual(s.stbm, "12345")
